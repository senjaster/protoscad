import trimesh
from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from manifold_learn.ast.evaluator import TreeEvaluator
from manifold_learn.ast.manifold import CubeModule, TranslateModule, IdentityModule
from manifold_learn.ast.tree_node import TreeNode
from manifold_learn.grammar.OpenSCADLexer import OpenSCADLexer
from manifold_learn.grammar.OpenSCADParser import OpenSCADParser


def parse_scad_with_errors(source: str) -> tuple[TreeNode, list[str]]:
    """Parse source, returning (root, list of syntax error messages)."""
    errors: list[str] = []

    class Collector(ErrorListener):
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            errors.append(msg)

    lexer = OpenSCADLexer(InputStream(source))
    lexer.removeErrorListeners()
    lexer.addErrorListener(Collector())
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(Collector())
    tree = parser.start()
    from manifold_learn.ast_visitor import AstOpenSCADVisitor

    root = AstOpenSCADVisitor().visit(tree)
    return root, errors

def manifold2trimesh(manifold):
    mesh = manifold.to_mesh()

    if mesh.vert_properties.shape[1] > 3:
        vertices = mesh.vert_properties[:, :3]
        colors = (mesh.vert_properties[:, 3:] * 255).astype(np.uint8)
    else:
        vertices = mesh.vert_properties
        colors = None

    return trimesh.Trimesh(
        vertices=vertices,
        faces=mesh.tri_verts,
        vertex_colors=colors
    )

def test_cube_creation():
    builtins = [
        IdentityModule("root"),
        IdentityModule("block"),
        CubeModule(),
        TranslateModule(),
    ]
    evaluator = TreeEvaluator(builtins)
    tree, errors = parse_scad_with_errors("translate([2,0,0]) cube([1.0,1.0,1.0]); cube(1);")
    result = evaluator.eval_tree(tree)
    mesh = manifold2trimesh(result)
    trimesh.exchange.export.export_mesh(mesh, "cube4.stl", "stl")