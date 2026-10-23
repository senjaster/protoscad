from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from manifold_learn.ast.expression import ArrayLiteral, Assignment, BinaryOp, NumberLiteral, Paren, Variable
from manifold_learn.ast.tree_node import TreeNode
from manifold_learn.grammar.OpenSCADLexer import OpenSCADLexer
from manifold_learn.grammar.OpenSCADParser import OpenSCADParser

from conftest import parse_scad

# A rich, nested, multi-statement OpenSCAD program exercising chained module
# calls, blocks, let bindings, array literals, variable redefinition and
# scope shadowing.
COMPLEX_SOURCE = """\
// Top-level variables
width = 10;
depth = width * 2;
height = (depth + 5) / 2;

scale([1, 2, 1])
translate([width, depth, height]) {
    box(5, center=true);
    cylinder(r=3, h=height, center=true);
    /* nested block */
    {
        sphere(2);
        translate([0, 0, 1]) cube([1, 1, 1]);
    }
}

let(offset = 4) {
    translate([0, 0, offset]) {
        box(offset);
    }
}

rotate([0, 0, 45]) box(width, center=true);

// Redefine width in the top-level scope: the old definition is discarded
width = 100;

// A block that shadows `width` with a local definition referencing the
// parent-scope value on its right-hand side (valid in OpenSCAD).
{
    width = width / 2;
    box(width);
}
"""


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


def find_modules(node: TreeNode, name: str) -> list[TreeNode]:
    """Return all descendant nodes (depth-first) with the given module name."""
    found = []
    for child in node.children:
        if child.module == name:
            found.append(child)
        found.extend(find_modules(child, name))
    return found


def test_complex_source_satisfies_grammar():
    _, errors = parse_scad_with_errors(COMPLEX_SOURCE)
    assert errors == []


def test_top_level_statements_are_children_of_root():
    root = parse_scad(COMPLEX_SOURCE)
    # Assignments register variables (no child nodes); the scale chain, let,
    # rotate chain, and the trailing shadowing block materialize as children.
    assert [c.module for c in root.children] == ["scale", "let", "rotate", "block"]


def test_chained_scale_translate_box_nesting():
    root = parse_scad(COMPLEX_SOURCE)
    scale = root.children[0]
    assert scale.module == "scale"
    # Array literal builds a list of element expressions
    assert scale.positional_args == [ArrayLiteral([NumberLiteral(1.0), NumberLiteral(2.0), NumberLiteral(1.0)])]

    translate = scale.children[0]
    assert translate.module == "translate"
    # The array literal [width, depth, height] resolves to variables
    assert translate.positional_args == [ArrayLiteral([Variable("width"), Variable("depth"), Variable("height")])]

    # The translate body is a block with box, cylinder, and a nested block.
    block = translate.children[0]
    assert block.module == "block"
    assert [c.module for c in block.children] == ["box", "cylinder", "block"]

    # box uses a named arg center=true
    box = block.children[0]
    assert box.module == "box"
    assert box.positional_args == [NumberLiteral(5.0)]
    assert box.named_args == {"center": Variable("true")}

    # cylinder uses named r, h, center
    cylinder = block.children[1]
    assert cylinder.module == "cylinder"
    assert cylinder.named_args == {
        "r": NumberLiteral(3.0),
        "h": Variable("height"),
        "center": Variable("true"),
    }

    # Nested block holds sphere and a translate->cube chain
    nested = block.children[2]
    assert nested.module == "block"
    assert [c.module for c in nested.children] == ["sphere", "translate"]
    sphere = nested.children[0]
    assert sphere.positional_args == [NumberLiteral(2.0)]
    inner_translate = nested.children[1]
    assert inner_translate.positional_args == [ArrayLiteral([NumberLiteral(0.0), NumberLiteral(0.0), NumberLiteral(1.0)])]
    cube = inner_translate.children[0]
    assert cube.module == "cube"
    assert cube.positional_args == [ArrayLiteral([NumberLiteral(1.0), NumberLiteral(1.0), NumberLiteral(1.0)])]


def test_let_binding_registers_on_let_node():
    root = parse_scad(COMPLEX_SOURCE)
    let_node = root.children[1]
    assert let_node.module == "let"
    assert let_node.variables == {"offset": Assignment("offset", NumberLiteral(4.0))}

    # let -> block -> translate -> block -> box
    block = let_node.children[0]
    assert block.module == "block"
    translate = block.children[0]
    assert translate.module == "translate"
    assert translate.positional_args == [ArrayLiteral([NumberLiteral(0.0), NumberLiteral(0.0), Variable("offset")])]
    inner_block = translate.children[0]
    assert inner_block.module == "block"
    box = inner_block.children[0]
    assert box.module == "box"
    # box(offset) references the let-bound variable
    assert box.positional_args == [Variable("offset")]


def test_top_level_assignments_register_on_root():
    # Top-level assignments register variable data on the root node;
    # resolution semantics are covered by the evaluator tests.
    root = parse_scad(COMPLEX_SOURCE)
    # width is redefined to 100 later in the source; the last definition
    # wins in the scope's variable table.
    assert root.variables["width"] == Assignment("width", NumberLiteral(100.0))
    assert set(root.variables) == {"width", "depth", "height"}
    # A let-bound variable is registered on the let node, not the root
    assert "offset" not in root.variables


def test_rotate_chain_uses_top_level_variable():
    root = parse_scad(COMPLEX_SOURCE)
    rotate = root.children[2]
    assert rotate.module == "rotate"
    assert rotate.positional_args == [ArrayLiteral([NumberLiteral(0.0), NumberLiteral(0.0), NumberLiteral(45.0)])]
    box = rotate.children[0]
    assert box.module == "box"
    # box(width, center=true): width is a Variable reference (resolves to 100)
    assert box.positional_args == [Variable("width")]
    assert box.named_args == {"center": Variable("true")}


def test_parent_links_are_consistent():
    root = parse_scad(COMPLEX_SOURCE)
    stack = [root]
    while stack:
        current = stack.pop()
        for child in current.children:
            assert child.parent is current
            stack.append(child)


def test_all_module_calls_have_expected_count():
    root = parse_scad(COMPLEX_SOURCE)
    assert len(find_modules(root, "cube")) == 1
    # box appears in the scale block, the let block, and the shadowing block
    assert len(find_modules(root, "box")) == 4
    assert len(find_modules(root, "sphere")) == 1
    assert len(find_modules(root, "cylinder")) == 1
    assert len(find_modules(root, "translate")) == 3


def test_shadowing_block_redefines_width_locally():
    # The trailing block redefines `width` locally, referencing the parent
    # scope's width on the right-hand side: width = width / 2. Resolution
    # semantics are covered by the evaluator tests; here we check the tree
    # carries both the redefinition and the reference.
    root = parse_scad(COMPLEX_SOURCE)
    shadow_block = root.children[3]
    assert shadow_block.module == "block"
    assert shadow_block.variables["width"] == Assignment(
        "width",
        BinaryOp("/", Variable("width"), NumberLiteral(2.0)),
    )
    # The top level keeps its own definition
    assert root.variables["width"] == Assignment("width", NumberLiteral(100.0))
    # The block's box(width) references the locally shadowed value
    box = shadow_block.children[0]
    assert box.module == "box"
    assert box.positional_args == [Variable("width")]