from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream

from protoscad.grammar.OpenSCADLexer import OpenSCADLexer
from protoscad.grammar.OpenSCADParser import OpenSCADParser
from protoscad.tree.expression import BinaryOp, NumberLiteral, Variable
from protoscad.tree.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    SourceSpan,
    VariableBindingStatement,
)
from protoscad.tree.visitor import AstOpenSCADVisitor

# A small program whose spans are easy to reason about. Lines are 1-based,
# columns 0-based (ANTLR convention).
SOURCE = """\
module Foo(a, b=2) {
    cube([10, 10, 10]);
}
x = 10;
let(y=5) {
    sphere(y);
}
"""


def parse_scad(source: str) -> ModuleCallStatement:
    """Parse source via the OpenSCAD grammar, returning the root scope call."""
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


def span(node) -> SourceSpan | None:
    return node.span


def test_module_call_span():
    scope = parse_scad(SOURCE)
    definition = scope.children[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    cube = definition.body.children[0]
    assert isinstance(cube, ModuleCallStatement)
    assert cube.module == "cube"
    assert span(cube) == SourceSpan(2, 4, 2, 22)


def test_module_definition_span():
    scope = parse_scad(SOURCE)
    definition = scope.children[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    assert definition.name == "Foo"
    # The `module` keyword starts at line 1 col 0; the closing `}` ends it.
    assert span(definition) == SourceSpan(1, 0, 3, 1)


def test_module_definition_body_scope_span():
    scope = parse_scad(SOURCE)
    definition = scope.children[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    # The synthesized `union` body covers the `{ ... }` block.
    assert span(definition.body) == SourceSpan(1, 19, 3, 1)


def test_variable_binding_span():
    scope = parse_scad(SOURCE)
    binding = scope.children[1]
    assert isinstance(binding, VariableBindingStatement)
    assert binding.name == "x"
    assert span(binding) == SourceSpan(4, 0, 4, 7)


def test_let_scope_and_binding_spans():
    scope = parse_scad(SOURCE)
    let_node = scope.children[2]
    assert isinstance(let_node, ModuleCallStatement)
    assert let_node.module == "let"
    # The let node covers `let(y=5)`, not its block.
    assert span(let_node) == SourceSpan(5, 0, 5, 8)

    binding = let_node.children[0]
    assert isinstance(binding, VariableBindingStatement)
    assert binding.name == "y"
    assert span(binding) == SourceSpan(5, 4, 5, 7)

    sphere = let_node.children[1]
    assert isinstance(sphere, ModuleCallStatement)
    assert sphere.module == "sphere"
    assert span(sphere) == SourceSpan(6, 4, 6, 13)


def test_root_scope_span_covers_children():
    scope = parse_scad(SOURCE)
    # The synthesized root `union` spans from the first statement's start to
    # the last statement's end.
    assert span(scope) == SourceSpan(1, 0, 5, 8)


def test_empty_source_root_has_no_span():
    scope = parse_scad("")
    assert scope.module == "union"
    assert scope.children == []
    assert span(scope) is None


def test_multiline_call_span_spans_lines():
    source = "translate([1, 2])\n    cube(10);\n"
    scope = parse_scad(source)
    translate = scope.children[0]
    assert isinstance(translate, ModuleCallStatement)
    assert translate.module == "translate"
    # `translate` starts on line 1; its `(`/`)` close on line 1 too.
    assert span(translate) == SourceSpan(1, 0, 1, 17)
    cube = translate.children[0]
    assert isinstance(cube, ModuleCallStatement)
    assert cube.module == "cube"
    assert span(cube) == SourceSpan(2, 4, 2, 12)


def test_variable_and_binary_op_expression_spans():
    scope = parse_scad(SOURCE)
    # `let(y=5)` then `sphere(y)`: the argument `y` is a Variable whose span
    # is the identifier itself.
    let_node = scope.children[2]
    assert isinstance(let_node, ModuleCallStatement)
    sphere = let_node.children[1]
    assert isinstance(sphere, ModuleCallStatement)
    argument = sphere.positional_args[0]
    assert isinstance(argument, Variable)
    assert argument.span == SourceSpan(6, 11, 6, 12)


def test_binary_op_span_and_fold_span_preservation():
    # `1 + 2 * 3` folds all the way down: the folded `2 * 3` literal keeps
    # the operand span, which lets the outer sum fold too, and the final
    # literal keeps the whole expression's span.
    scope = parse_scad("x = 1 + 2 * 3;\n")
    binding = scope.children[0]
    assert isinstance(binding, VariableBindingStatement)
    value = binding.value
    assert isinstance(value, NumberLiteral)
    assert value.value == 7.0
    assert value.span == SourceSpan(1, 4, 1, 13)


def test_binary_op_partial_fold_keeps_operation_and_spans():
    # A variable operand stops the fold, but the constant sub-expression
    # still collapses and carries its own span.
    scope = parse_scad("x = y + 2 * 3;\n")
    binding = scope.children[0]
    assert isinstance(binding, VariableBindingStatement)
    value = binding.value
    assert isinstance(value, BinaryOp)
    assert value.span == SourceSpan(1, 4, 1, 13)
    assert isinstance(value.left, Variable)
    assert value.left.span == SourceSpan(1, 4, 1, 5)
    right = value.right
    assert isinstance(right, NumberLiteral)
    assert right.value == 6.0
    assert right.span == SourceSpan(1, 8, 1, 13)


def test_named_arg_span_covers_name_and_value():
    scope = parse_scad("cube(center = true);\n")
    call = scope.children[0]
    assert isinstance(call, ModuleCallStatement)
    center = call.named_args["center"]
    # The argument's span is the whole `center = true`, not just the value.
    assert center.span == SourceSpan(1, 5, 1, 18)


def test_if_statement_span_covers_the_whole_construct():
    scope = parse_scad("if (x) cube(1);\n")
    if_call = scope.children[0]
    assert isinstance(if_call, ModuleCallStatement)
    assert if_call.module == "if"
    assert span(if_call) == SourceSpan(1, 0, 1, 15)
    condition = if_call.positional_args[0]
    assert isinstance(condition, Variable)
    assert condition.span == SourceSpan(1, 4, 1, 5)


def test_if_else_span_extends_through_the_else_branch():
    scope = parse_scad("if (x) cube(1);\nelse sphere(2);\n")
    if_call = scope.children[0]
    assert span(if_call) == SourceSpan(1, 0, 2, 15)
    else_scope = if_call.children[1]
    assert else_scope.module == "union"
    # The branch scope's span is its body, like a module body's — the
    # `else` keyword itself is not part of the scope.
    assert span(else_scope) == SourceSpan(2, 5, 2, 15)
    (else_call,) = else_scope.children
    assert else_call.span == SourceSpan(2, 5, 2, 14)
