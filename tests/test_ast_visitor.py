from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from manifold_learn.ast.expression import BinaryOp, NumberLiteral, Paren, Raw, Variable
from manifold_learn.ast.tree_node import TreeNode
from manifold_learn.grammar.OpenSCADLexer import OpenSCADLexer
from manifold_learn.grammar.OpenSCADParser import OpenSCADParser

from conftest import parse_scad


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


def single_child(root: TreeNode) -> TreeNode:
    assert len(root.children) == 1
    return root.children[0]


def test_single_module_call():
    root = parse_scad("cube(10);")
    node = single_child(root)
    assert node.module == "cube"
    assert node.positional_args == [NumberLiteral(10.0)]
    assert node.named_args == {}


def test_module_call_no_args():
    root = parse_scad("cube();")
    node = single_child(root)
    assert node.module == "cube"
    assert node.positional_args == []
    assert node.named_args == {}


def test_named_args():
    root = parse_scad("cylinder(r=5, h=10);")
    node = single_child(root)
    assert node.module == "cylinder"
    assert node.positional_args == []
    assert node.named_args == {
        "r": NumberLiteral(5.0),
        "h": NumberLiteral(10.0),
    }


def test_mixed_positional_and_named_args():
    root = parse_scad("cube([10,10,10], center=true);")
    node = single_child(root)
    assert node.module == "cube"
    assert node.positional_args == [Raw("[10,10,10]")]
    assert node.named_args == {"center": Variable("true")}


def test_chained_module_calls_nest():
    root = parse_scad("translate([1,2,3]) rotate([0,0,45]) cube([10,10,10]);")
    translate = single_child(root)
    assert translate.module == "translate"
    assert len(translate.children) == 1
    rotate = translate.children[0]
    assert rotate.module == "rotate"
    assert len(rotate.children) == 1
    cube = rotate.children[0]
    assert cube.module == "cube"
    assert cube.parent is rotate


def test_block_children():
    root = parse_scad("{ cube(1); sphere(2); }")
    block = single_child(root)
    assert block.module == "block"
    assert [c.module for c in block.children] == ["cube", "sphere"]


def test_nested_blocks():
    root = parse_scad("{ cube(1); { sphere(2); } }")
    block = single_child(root)
    assert [c.module for c in block.children] == ["cube", "block"]
    inner = block.children[1]
    assert [c.module for c in inner.children] == ["sphere"]


def test_let_binding_variable_visible_to_child():
    root = parse_scad("let(x=10) { cube(x); }")
    let_node = single_child(root)
    assert let_node.module == "let"
    # Binding stored as a variable on the let node
    assert let_node.eval_variable("x") == 10.0
    # The block body is a child of the let node
    block = let_node.children[0]
    assert block.module == "block"
    cube = block.children[0]
    assert cube.module == "cube"
    # Child resolves the variable through the parent scope chain
    assert cube.positional_args == [Variable("x")]
    assert cube.eval_variable("x") == 10.0


def test_module_definition_produces_tree_node():
    root = parse_scad(
        "module Foo(a, b=2) { cube(a); sphere(b); }"
    )
    # A module definition is represented as a tree node named after the
    # module, with its body attached as a child.
    assert len(root.children) == 1
    foo = root.children[0]
    assert foo.module == "Foo"
    assert foo.positional_args == []
    assert foo.named_args == {}


def test_assignment_registers_variable_on_scope():
    root = parse_scad("var1 = (10+20)/3;")
    # An assignment defines a variable on the enclosing scope rather than
    # adding a child node.
    assert root.children == []
    assert root.eval_variable("var1") == 10.0


def test_assignment_inside_block_scopes_to_block():
    # An assignment inside a block registers on the block node, not the root.
    root = parse_scad("{ local = 7; cube(local); }")
    block = root.children[0]
    assert block.module == "block"
    assert block.eval_variable("local") == 7.0
    # The variable is scoped to the block, not visible at the top level
    assert root.eval_variable("local") is None
    cube = block.children[0]
    assert cube.positional_args == [Variable("local")]
    assert cube.eval_variable("local") == 7.0


def test_let_expression_shapes():
    # A let binding can itself be a binary expression over literals
    root = parse_scad("let(x = (10 + 20) / 3) { cube(x); }")
    let_node = root.children[0]
    assert let_node.module == "let"
    assert let_node.eval_variable("x") == 10.0
    cube = let_node.children[0].children[0]
    assert cube.positional_args == [Variable("x")]
    assert cube.eval_variable("x") == 10.0


def test_number_expression():
    root = parse_scad("cube(3.5);")
    node = single_child(root)
    assert node.positional_args == [NumberLiteral(3.5)]


def test_variable_expression():
    root = parse_scad("cube(size);")
    node = single_child(root)
    assert node.positional_args == [Variable("size")]


def test_additive_expression():
    root = parse_scad("cube(10+20);")
    node = single_child(root)
    expr = node.positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "+"
    assert expr.left == NumberLiteral(10.0)
    assert expr.right == NumberLiteral(20.0)


def test_multiplicative_expression():
    root = parse_scad("cube(10*20);")
    node = single_child(root)
    expr = node.positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "*"


def test_paren_expression():
    root = parse_scad("cube((10+20)/3);")
    node = single_child(root)
    expr = node.positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "/"
    # Left operand is a Paren wrapping an additive BinaryOp
    assert isinstance(expr.left, Paren)
    assert isinstance(expr.left.inner, BinaryOp)
    assert expr.left.inner.op == "+"


def test_array_literal_is_raw_stub():
    root = parse_scad("cube([12, var2+2, -3.2]);")
    node = single_child(root)
    # Raw captures the token text; whitespace between tokens is not preserved
    assert node.positional_args == [Raw("[12,var2+2,-3.2]")]


def test_comments_are_ignored():
    root = parse_scad(
        "// line comment\n"
        "cube(1);\n"
        "/* block\n"
        "comment */\n"
        "sphere(2);\n"
    )
    assert [c.module for c in root.children] == ["cube", "sphere"]


def test_named_arg_before_positional_is_rejected():
    root, errors = parse_scad_with_errors("foo(bar=2, 1);")
    assert errors, "expected a syntax error for named-before-positional args"


def test_valid_mixed_args_produce_no_errors():
    _, errors = parse_scad_with_errors("foo(1, 2, r=5);")
    assert errors == []