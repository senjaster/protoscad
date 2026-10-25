import click
import trimesh
from antlr4 import CommonTokenStream, InputStream

from manifold_learn.builtins import BUILTIN_MODULES
from manifold_learn.grammar.OpenSCADLexer import OpenSCADLexer
from manifold_learn.grammar.OpenSCADParser import OpenSCADParser
from manifold_learn.runtime.evaluator import StatementEvaluator
from manifold_learn.tree import AstOpenSCADVisitor, ModuleCallStatement


def parse_scad(source: str) -> ModuleCallStatement:
    """Parse source via the OpenSCAD grammar, returning the root scope call."""
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)

# Helper to convert a Manifold into a Trimesh
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
@click.argument('filename', type=click.Path(exists=True))
def render(filename: str):
    print(filename)
    with open(filename) as f:
        content = f.read()
    ast = parse_scad(content)
    modules =(c() for c in BUILTIN_MODULES)
    evaluator = StatementEvaluator(modules)
    manifold = evaluator.evaluate(ast)
    mesh = manifold2trimesh(manifold)
    mesh.show()
    # trimesh.exchange.export.export_mesh(mesh, "cube2.stl", "stl")

if __name__ == '__main__':
    render()
