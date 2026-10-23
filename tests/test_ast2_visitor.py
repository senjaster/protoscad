from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from manifold_learn.ast.expression import ArrayLiteral, Assignment, BinaryOp, NumberLiteral, Paren, Undefined, Variable
from manifold_learn.ast.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    Statement,
    VariableBindingStatement,
)
from manifold_learn.ast.visitor import AstOpenSCADVisitor
from manifold_learn.grammar.OpenSCADLexer import OpenSCADLexer
from manifold_learn.grammar.OpenSCADParser import OpenSCADParser


def parse_scad(source: str) -> list[Statement]:
    """Parse source via the OpenSCAD grammar, returning a scope (statement list)."""
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


def parse_scad_with_errors(source: str) -> tuple[list[Statement], list[str]]:
    """Parse source, returning (scope, list of syntax error messages)."""
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
    scope = AstOpenSCADVisitor().visit(tree)
    return scope, errors


def single_call(scope: list[Statement]) -> ModuleCallStatement:
    assert len(scope) == 1
    assert isinstance(scope[0], ModuleCallStatement)
    return scope[0]


## =========================================================================
#  Basic module calls


def test_single_module_call():
    scope = parse_scad("cube(10);")
    node = single_call(scope)
    assert node.module == "cube"
    assert node.positional_args == [NumberLiteral(10.0)]
    assert node.named_args == {}


def test_module_call_no_args():
    scope = parse_scad("cube();")
    node = single_call(scope)
    assert node.module == "cube"
    assert node.positional_args == []
    assert node.named_args == {}


def test_named_args():
    scope = parse_scad("cylinder(r=5, h=10);")
    node = single_call(scope)
    assert node.module == "cylinder"
    assert node.named_args == {"r": NumberLiteral(5.0), "h": NumberLiteral(10.0)}


def test_mixed_positional_and_named_args():
    scope = parse_scad("cube([10,10,10], center=true);")
    node = single_call(scope)
    assert node.positional_args == [
        ArrayLiteral([NumberLiteral(10.0), NumberLiteral(10.0), NumberLiteral(10.0)])
    ]
    assert node.named_args == {"center": Variable("true")}


def test_chained_module_calls_nest():
    scope = parse_scad("translate([1,2,3]) rotate([0,0,45]) cube([10,10,10]);")
    translate = single_call(scope)
    assert translate.module == "translate"
    assert len(translate.children) == 1
    rotate = translate.children[0]
    assert isinstance(rotate, ModuleCallStatement)
    assert rotate.module == "rotate"
    assert len(rotate.children) == 1
    cube = rotate.children[0]
    assert isinstance(cube, ModuleCallStatement)
    assert cube.module == "cube"


## =========================================================================
#  Blocks are transparent (spliced)


def test_bare_block_splices_into_scope():
    scope = parse_scad("{ cube(1); sphere(2); }")
    # The bare block contributes its calls directly to the enclosing scope.
    assert [s.module for s in scope] == ["cube", "sphere"]


def test_nested_bare_blocks_splice():
    scope = parse_scad("{ cube(1); { sphere(2); } }")
    assert [s.module for s in scope] == ["cube", "sphere"]


## =========================================================================
#  Module call bodies


def test_call_with_block_body():
    scope = parse_scad("translate([1,2,3]) { cube(1); sphere(2); }")
    translate = single_call(scope)
    assert [s.module for s in translate.children] == ["cube", "sphere"]


def test_call_with_braced_block_is_single_child():
    # QUIRKS.md: a module invocation `union() { ... }` is a single child, even
    # though a bare `{ ... }` block is transparent.
    scope = parse_scad(
        'module my_mod() { children(1); } my_mod() { echo("aaa"); union() { echo("bbb"); echo("ccc"); } }'
    )
    call = scope[1]
    assert isinstance(call, ModuleCallStatement)
    assert [s.module for s in call.children] == ["echo", "union"]
    union = call.children[1]
    assert isinstance(union, ModuleCallStatement)
    assert union.children[0].module == "echo"


def test_bare_block_inside_call_body_is_unwrapped():
    # QUIRKS.md: children(1) yields `bbb` only, because the bare block is
    # unwrapped and contributes `bbb` and `ccc` as two separate children.
    scope = parse_scad(
        'module my_mod() { children(1); } my_mod() { echo("aaa"); { echo("bbb"); echo("ccc"); } }'
    )
    call = scope[1]
    assert isinstance(call, ModuleCallStatement)
    assert [s.module for s in call.children] == ["echo", "echo", "echo"]


## =========================================================================
#  Module definitions


def test_module_definition_body_is_a_list():
    # QUIRKS.md: a module body is a list of statements, with variable bindings
    # and module calls side by side.
    scope = parse_scad("module x() { aaa(); bbb(); x = 10; }")
    assert len(scope) == 1
    definition = scope[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    assert definition.name == "x"
    assert isinstance(definition.body, list)
    assert [type(s).__name__ for s in definition.body] == [
        "ModuleCallStatement",
        "ModuleCallStatement",
        "VariableBindingStatement",
    ]
    assert isinstance(definition.body[2], VariableBindingStatement)
    assert definition.body[2].name == "x"
    assert definition.body[2].value == NumberLiteral(10.0)


def test_module_definition_parameters():
    scope = parse_scad("module Foo(a, b=2) { cube(a); }")
    definition = scope[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    assert set(definition.parameters) == {"a", "b"}
    assert definition.parameters["a"] == Assignment("a", Undefined())
    assert definition.parameters["b"] == Assignment("b", NumberLiteral(2.0))


def test_module_definition_braced_less_body():
    # A brace-less body is a simplified body of one statement.
    scope = parse_scad("module x() cube(1);")
    definition = scope[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    assert len(definition.body) == 1
    assert isinstance(definition.body[0], ModuleCallStatement)
    assert definition.body[0].module == "cube"


def test_module_definition_inside_block_scopes_to_block():
    scope = parse_scad("{ module Bar() { cube(1); } Bar(); }")
    # Bare block is transparent, so the definition and call land in the
    # top-level scope.
    assert [type(s).__name__ for s in scope] == [
        "ModuleDefinitionStatement",
        "ModuleCallStatement",
    ]


## =========================================================================
#  let bindings


def test_let_binding_becomes_variable_binding_statement():
    # `let` is a scope: its bindings become leading VariableBindingStatements
    # in the let node's body, followed by the visited continuation.
    scope = parse_scad("let(x=10) { cube(x); }")
    let_node = single_call(scope)
    assert let_node.module == "let"
    assert isinstance(let_node.children[0], VariableBindingStatement)
    assert let_node.children[0].name == "x"
    assert let_node.children[0].value == NumberLiteral(10.0)
    assert isinstance(let_node.children[1], ModuleCallStatement)
    assert let_node.children[1].module == "cube"
    assert let_node.children[1].positional_args == [Variable("x")]


def test_let_multiple_bindings():
    scope = parse_scad("let(a=1, b=2) { cube(a); }")
    let_node = single_call(scope)
    assert [s.name for s in let_node.children if isinstance(s, VariableBindingStatement)] == ["a", "b"]


## =========================================================================
#  Assignments


def test_assignment_is_variable_binding_statement():
    scope = parse_scad("var1 = (10+20)/3;")
    assert len(scope) == 1
    binding = scope[0]
    assert isinstance(binding, VariableBindingStatement)
    assert binding.name == "var1"
    assert binding.value == BinaryOp(
        "/",
        Paren(BinaryOp("+", NumberLiteral(10.0), NumberLiteral(20.0))),
        NumberLiteral(3.0),
    )


def test_assignment_inside_block_scopes_to_enclosing_scope():
    # A bare block is transparent, so `local` binds in the top-level scope.
    scope = parse_scad("{ local = 7; cube(local); }")
    assert [type(s).__name__ for s in scope] == [
        "VariableBindingStatement",
        "ModuleCallStatement",
    ]
    binding = scope[0]
    assert isinstance(binding, VariableBindingStatement)
    assert binding.name == "local"
    assert binding.value == NumberLiteral(7.0)


## =========================================================================
#  Expressions (mirror the existing expression coverage)


def test_number_expression():
    scope = parse_scad("cube(3.5);")
    assert single_call(scope).positional_args == [NumberLiteral(3.5)]


def test_variable_expression():
    scope = parse_scad("cube(size);")
    assert single_call(scope).positional_args == [Variable("size")]


def test_additive_expression():
    scope = parse_scad("cube(10+20);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "+"
    assert expr.left == NumberLiteral(10.0)
    assert expr.right == NumberLiteral(20.0)


def test_multiplicative_expression():
    scope = parse_scad("cube(10*20);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "*"


def test_paren_expression():
    scope = parse_scad("cube((10+20)/3);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "/"
    assert isinstance(expr.left, Paren)
    assert isinstance(expr.left.inner, BinaryOp)
    assert expr.left.inner.op == "+"


def test_array_literal_builds_list_of_expressions():
    scope = parse_scad("cube([12, var2+2, -3.2]);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, ArrayLiteral)
    assert expr.elements == [
        NumberLiteral(12.0),
        BinaryOp("+", Variable("var2"), NumberLiteral(2.0)),
        NumberLiteral(-3.2),
    ]


def test_empty_array_literal():
    scope = parse_scad("cube([]);")
    assert single_call(scope).positional_args == [ArrayLiteral([])]


def test_comments_are_ignored():
    scope = parse_scad(
        "// line comment\n"
        "cube(1);\n"
        "/* block\n"
        "comment */\n"
        "sphere(2);\n"
    )
    assert [s.module for s in scope] == ["cube", "sphere"]


## =========================================================================
#  Syntax rejection


def test_named_arg_before_positional_is_rejected():
    _, errors = parse_scad_with_errors("foo(bar=2, 1);")
    assert errors, "expected a syntax error for named-before-positional args"


def test_valid_mixed_args_produce_no_errors():
    _, errors = parse_scad_with_errors("foo(1, 2, r=5);")
    assert errors == []