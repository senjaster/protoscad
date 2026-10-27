import sys

import click
import numpy as np
import trimesh

from protoscad.builtins import BUILTIN_MODULES
from protoscad.diagnostics import Diagnostic, ProtoSCADError, render_json, render_text
from protoscad.parser import parse_scad
from protoscad.runtime.evaluator import evaluate


def manifold2trimesh(manifold):
    mesh = manifold.to_mesh()

    if mesh.vert_properties.shape[1] > 3:
        vertices = mesh.vert_properties[:, :3]
        colors = (mesh.vert_properties[:, 3:] * 255).astype(np.uint8)
    else:
        vertices = mesh.vert_properties
        colors = None

    return trimesh.Trimesh(vertices=vertices, faces=mesh.tri_verts, vertex_colors=colors)


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False),
    help="Save the result as an STL file instead of showing it on screen.",
)
@click.option(
    "--err-format",
    "err_format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Error reporting format: human-readable text (stderr) or JSON for tooling (stdout).",
)
def render(filename: str, output: str | None, err_format: str) -> None:
    """Render an OpenSCAD file, showing it on screen or saving it as STL."""
    with open(filename) as f:
        content = f.read()
    try:
        ast = parse_scad(content)
        modules = (c() for c in BUILTIN_MODULES)
        manifold = evaluate(ast, modules)
        mesh = manifold2trimesh(manifold)
    except ProtoSCADError as error:
        _report_error(error.diagnostic, content, filename, err_format)
        sys.exit(1)

    if output is not None:
        trimesh.exchange.export.export_mesh(mesh, output, "stl")
    else:
        mesh.show()


def _report_error(diagnostic: Diagnostic, source: str, filename: str, format_: str) -> None:
    # JSON goes to stdout so tooling can consume it unpolluted; text goes to
    # stderr like the rest of the diagnostics.
    if format_ == "json":
        click.echo(render_json([diagnostic], file=filename))
    else:
        click.echo(render_text([diagnostic], source, file=filename), err=True)


if __name__ == "__main__":
    render()
