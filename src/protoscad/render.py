import click
import numpy as np
import trimesh
from antlr4 import CommonTokenStream, InputStream

from protoscad.builtins import BUILTIN_MODULES
from protoscad.grammar.OpenSCADLexer import OpenSCADLexer
from protoscad.grammar.OpenSCADParser import OpenSCADParser
from protoscad.runtime.evaluator import evaluate
from protoscad.tree import AstOpenSCADVisitor, ModuleCallStatement


def parse_scad(source: str) -> ModuleCallStatement:
    """Parse source via the OpenSCAD grammar, returning the root scope call."""
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


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
def render(filename: str, output: str | None) -> None:
    """Render an OpenSCAD file, showing it on screen or saving it as STL."""
    with open(filename) as f:
        content = f.read()
    ast = parse_scad(content)
    modules = (c() for c in BUILTIN_MODULES)
    manifold = evaluate(ast, modules)
    mesh = manifold2trimesh(manifold)

    if output is not None:
        trimesh.exchange.export.export_mesh(mesh, output, "stl")
    else:
        mesh.show()


if __name__ == "__main__":
    render()
