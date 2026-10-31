from __future__ import annotations

import json

from click.testing import CliRunner

from protoscad.render import render


def test_render_unknown_module_json_goes_to_stdout(tmp_path):
    scad = tmp_path / "bad.scad"
    scad.write_text("cube(1);\nsphare(2);\n")
    result = CliRunner().invoke(render, [str(scad), "--err-format", "json"])
    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    diagnostic = payload["diagnostics"][0]
    assert diagnostic["code"] == "unknown-module"
    assert diagnostic["file"] == str(scad)
    assert diagnostic["range"]["start"] == {"line": 1, "character": 0}


def test_render_syntax_error_text_goes_to_stderr(tmp_path):
    scad = tmp_path / "bad.scad"
    scad.write_text("cube(1;\n")
    result = CliRunner().invoke(render, [str(scad)])
    assert result.exit_code == 1
    assert "error[syntax]" in result.stderr
    assert "cube(1;" in result.stderr


def test_render_text_is_the_default_format(tmp_path):
    scad = tmp_path / "bad.scad"
    scad.write_text("sphare(2);\n")
    result = CliRunner().invoke(render, [str(scad)])
    assert result.exit_code == 1
    assert "error[unknown-module]: Unknown module: 'sphare'" in result.stderr
    assert "  --> " in result.stderr
    assert "sphare(2);" in result.stderr


def test_render_2d_toplevel_exports_svg_and_dxf(tmp_path):
    # 2D output reaches the vector formats, like OpenSCAD's DXF/SVG export.
    scad = tmp_path / "flat.scad"
    scad.write_text("square(5);\n")
    svg = tmp_path / "out.svg"
    dxf = tmp_path / "out.dxf"
    for target in (svg, dxf):
        result = CliRunner().invoke(render, [str(scad), "-o", str(target)])
        assert result.exit_code == 0

    svg_text = svg.read_text()
    assert svg_text.startswith("<svg")
    assert 'd="M' in svg_text  # a path from the square's contour

    dxf_text = dxf.read_text()
    assert "SECTION" in dxf_text and "ENTITIES" in dxf_text
    assert "LWPOLYLINE" in dxf_text


def test_render_export_refuses_dimension_format_mismatch(tmp_path):
    # STL exports solids, SVG/DXF export planes; the mismatch is refused
    # with a diagnostic (where OpenSCAD warns and skips) rather than a
    # guessed projection.
    flat = tmp_path / "flat.scad"
    flat.write_text("square(5);\n")
    solid = tmp_path / "solid.scad"
    solid.write_text("cube(5);\n")

    result = CliRunner().invoke(render, [str(flat), "-o", str(tmp_path / "out.stl")])
    assert result.exit_code == 1
    assert "error[export-format-mismatch]" in result.stderr
    assert "linear_extrude" in result.stderr

    result = CliRunner().invoke(render, [str(solid), "-o", str(tmp_path / "out.svg")])
    assert result.exit_code == 1
    assert "error[export-format-mismatch]" in result.stderr
    assert not (tmp_path / "out.svg").exists()
