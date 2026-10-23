import pytest
from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from manifold_learn.ast.evaluator import TreeEvaluator
from manifold_learn.ast.manifold import CubeModule, TranslateModule
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


def evaluate(source: str):
    tree, errors = parse_scad_with_errors(source)
    assert errors == []
    evaluator = TreeEvaluator([CubeModule(), TranslateModule()])
    return evaluator.evaluate(tree)


def test_translate_and_cubes_union(tmp_path):
    # Two disjoint unit cubes (the second shifted away) union to volume 2
    result = evaluate("translate([2,0,0]) cube([1.0,1.0,1.0]); cube(1);")
    assert result.volume() == pytest.approx(2.0)


def test_let_and_top_level_variables_end_to_end():
    result = evaluate("s = 2; let(offset = 5) { translate([offset,0,0]) cube(s); } cube(1);")
    # The unit cube sits fully inside the shifted 2-cube: union volume 8
    assert result.volume() == pytest.approx(8.0)


def test_stl_export_round_trip(tmp_path):
    import trimesh

    result = evaluate("cube(1);")
    mesh = result.to_mesh()
    trimesh_mesh = trimesh.Trimesh(
        vertices=mesh.vert_properties[:, :3],
        faces=mesh.tri_verts,
    )
    out = tmp_path / "cube.stl"
    trimesh.exchange.export.export_mesh(trimesh_mesh, out, "stl")
    loaded = trimesh.load_mesh(out)
    assert loaded.volume == pytest.approx(1.0)
