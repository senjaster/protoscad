import sys
from pathlib import Path

import click
import numpy as np
import trimesh
from manifold3d import CrossSection
from trimesh.path.entities import Line

from protoscad.builtins import BUILTIN_MODULES
from protoscad.diagnostics import Diagnostic, ErrorCode, ProtoSCADError, render_json, render_text
from protoscad.parser import parse_scad
from protoscad.runtime.evaluator import evaluate

# Vector formats the CLI can save 2D geometry in, keyed by file extension.
# Everything else goes down the solid (STL) path, as before.
EXPORT_2D_FORMATS = {".svg", ".dxf"}


def manifold2trimesh(manifold):
    mesh = manifold.to_mesh()

    if mesh.vert_properties.shape[1] > 3:
        vertices = mesh.vert_properties[:, :3]
        colors = (mesh.vert_properties[:, 3:] * 255).astype(np.uint8)
    else:
        vertices = mesh.vert_properties
        colors = None

    return trimesh.Trimesh(vertices=vertices, faces=mesh.tri_verts, vertex_colors=colors)


def crosssection2path(section):
    """A planar CrossSection as a trimesh Path2D: one closed polyline
    entity per contour, the shape trimesh's SVG/DXF exporters write."""
    entities = []
    vertices: list[list[float]] = []
    for contour in section.to_polygons():
        base = len(vertices)
        vertices.extend(contour.tolist())
        # Close the loop: manifold contours do not repeat the first vertex.
        entities.append(Line(points=[*range(base, len(vertices)), base]))
    return trimesh.path.Path2D(entities=entities, vertices=np.array(vertices) if vertices else np.empty((0, 2)))


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False),
    help="Save the result as STL (3D) or SVG/DXF (2D) instead of showing it on screen.",
)
@click.option(
    "--err-format",
    "err_format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Error reporting format: human-readable text (stderr) or JSON for tooling (stdout).",
)
def render(filename: str, output: str | None, err_format: str) -> None:
    """Render an OpenSCAD file, showing it on screen or saving it as STL/SVG/DXF."""
    with open(filename) as f:
        content = f.read()
    try:
        ast = parse_scad(content)
        modules = (c() for c in BUILTIN_MODULES)
        geometry = evaluate(ast, modules)
        if output is not None:
            _export(geometry, output)
        else:
            _show(geometry)
    except ProtoSCADError as error:
        _report_error(error.diagnostic, content, filename, err_format)
        sys.exit(1)


def _export(geometry, output: str) -> None:
    """Save geometry in the format the output's extension names.

    OpenSCAD's split: STL (and friends) export solids, SVG/DXF export 2D
    geometry. A mismatch is refused with a diagnostic — where OpenSCAD
    warns and skips the export — instead of guessing a projection.
    """
    extension = Path(output).suffix.lower()
    if extension in EXPORT_2D_FORMATS:
        if not isinstance(geometry, CrossSection):
            raise ProtoSCADError(
                f"Top-level geometry is 3D, but {extension[1:]} exports 2D geometry; export STL instead",
                code=ErrorCode.EXPORT_FORMAT_MISMATCH,
            )
        Path(output).write_text(crosssection2path(geometry).export(file_type=extension[1:]))
    else:
        if isinstance(geometry, CrossSection):
            raise ProtoSCADError(
                "Top-level geometry is 2D; STL exports 3D solids — wrap it in linear_extrude() or export .svg/.dxf",
                code=ErrorCode.EXPORT_FORMAT_MISMATCH,
            )
        trimesh.exchange.export.export_mesh(manifold2trimesh(geometry), output, "stl")


def _show(geometry) -> None:
    if isinstance(geometry, CrossSection):
        # The mesh viewer is solid-shaped; show the plane filled and flat,
        # the way OpenSCAD paints 2D, as a near-zero-thickness slab.
        xmin, ymin, xmax, ymax = geometry.bounds()
        thickness = max(xmax - xmin, ymax - ymin) / 100 or 0.1
        manifold2trimesh(geometry.extrude(thickness)).show()
    else:
        manifold2trimesh(geometry).show()


def _report_error(diagnostic: Diagnostic, source: str, filename: str, format_: str) -> None:
    # JSON goes to stdout so tooling can consume it unpolluted; text goes to
    # stderr like the rest of the diagnostics.
    if format_ == "json":
        click.echo(render_json([diagnostic], file=filename))
    else:
        click.echo(render_text([diagnostic], source, file=filename), err=True)


if __name__ == "__main__":
    render()
