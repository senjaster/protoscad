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
