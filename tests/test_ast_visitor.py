from __future__ import annotations

import pytest
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.grammar.OpenSCADLexer import OpenSCADLexer
from protoscad.grammar.OpenSCADParser import OpenSCADParser
from protoscad.tree.expression import (
    Assignment,
    BinaryOp,
    BooleanLiteral,
    Call,
    LetExpr,
    Literal,
    NumberLiteral,
    Paren,
    StringLiteral,
    TernaryOp,
    UnaryOp,
    Undefined,
    UndefLiteral,
    Variable,
    VectorLiteral,
)
from protoscad.tree.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    Statement,
    VariableBindingStatement,
)
from protoscad.tree.values import RangeValue
from protoscad.tree.visitor import AstOpenSCADVisitor


def parse_scad(source: str) -> ModuleCallStatement:
    """Parse source via the OpenSCAD grammar, returning the root scope call."""
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


def parse_scad_with_errors(source: str) -> tuple[ModuleCallStatement, list[str]]:
    """Parse source, returning (root scope call, list of syntax error messages)."""
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


def single_call(scope: ModuleCallStatement) -> ModuleCallStatement:
    assert len(scope.children) == 1
    assert isinstance(scope.children[0], ModuleCallStatement)
    return scope.children[0]


def call_names(children: list[Statement]) -> list[str]:
    """Module names of the calls among the statements — narrowing so the
    type checker sees ``ModuleCallStatement`` through the ``Statement`` list."""
    return [s.module for s in children if isinstance(s, ModuleCallStatement)]


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
    assert node.positional_args == [Literal([10.0, 10.0, 10.0])]
    assert node.named_args == {"center": BooleanLiteral(True)}


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
    assert call_names(scope.children) == ["cube", "sphere"]


def test_nested_bare_blocks_splice():
    scope = parse_scad("{ cube(1); { sphere(2); } }")
    assert call_names(scope.children) == ["cube", "sphere"]


## =========================================================================
#  Module call bodies


def test_call_with_block_body():
    scope = parse_scad("translate([1,2,3]) { cube(1); sphere(2); }")
    translate = single_call(scope)
    assert call_names(translate.children) == ["cube", "sphere"]


def test_call_with_braced_block_is_single_child():
    # QUIRKS.md: a module invocation `union() { ... }` is a single child, even
    # though a bare `{ ... }` block is transparent.
    scope = parse_scad(
        'module my_mod() { children(1); } my_mod() { echo("aaa"); union() { echo("bbb"); echo("ccc"); } }'
    )
    call = scope.children[1]
    assert isinstance(call, ModuleCallStatement)
    assert call_names(call.children) == ["echo", "union"]
    union = call.children[1]
    assert isinstance(union, ModuleCallStatement)
    first_child = union.children[0]
    assert isinstance(first_child, ModuleCallStatement)
    assert first_child.module == "echo"


def test_bare_block_inside_call_body_is_unwrapped():
    # QUIRKS.md: children(1) yields `bbb` only, because the bare block is
    # unwrapped and contributes `bbb` and `ccc` as two separate children.
    scope = parse_scad('module my_mod() { children(1); } my_mod() { echo("aaa"); { echo("bbb"); echo("ccc"); } }')
    call = scope.children[1]
    assert isinstance(call, ModuleCallStatement)
    assert call_names(call.children) == ["echo", "echo", "echo"]


## =========================================================================
#  Module definitions


def test_module_definition_body_is_a_scope_call():
    # QUIRKS.md: a module body is a scope call whose children are statements,
    # with variable bindings and module calls side by side.
    scope = parse_scad("module x() { aaa(); bbb(); x = 10; }")
    assert len(scope.children) == 1
    definition = scope.children[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    assert definition.name == "x"
    assert isinstance(definition.body, ModuleCallStatement)
    assert [type(s).__name__ for s in definition.body.children] == [
        "ModuleCallStatement",
        "ModuleCallStatement",
        "VariableBindingStatement",
    ]
    assert isinstance(definition.body.children[2], VariableBindingStatement)
    assert definition.body.children[2].name == "x"
    assert definition.body.children[2].value == NumberLiteral(10.0)


def test_module_definition_parameters():
    scope = parse_scad("module Foo(a, b=2) { cube(a); }")
    definition = scope.children[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    assert set(definition.parameters) == {"a", "b"}
    assert definition.parameters["a"] == Assignment("a", Undefined())
    assert definition.parameters["b"] == Assignment("b", NumberLiteral(2.0))


def test_module_definition_braced_less_body():
    # A brace-less body is a simplified body of one statement.
    scope = parse_scad("module x() cube(1);")
    definition = scope.children[0]
    assert isinstance(definition, ModuleDefinitionStatement)
    assert len(definition.body.children) == 1
    assert isinstance(definition.body.children[0], ModuleCallStatement)
    assert definition.body.children[0].module == "cube"


def test_module_definition_inside_block_scopes_to_block():
    scope = parse_scad("{ module Bar() { cube(1); } Bar(); }")
    # Bare block is transparent, so the definition and call land in the
    # top-level scope.
    assert [type(s).__name__ for s in scope.children] == [
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
    assert [s.name for s in let_node.children if isinstance(s, VariableBindingStatement)] == [
        "a",
        "b",
    ]


## =========================================================================
#  Assignments


def test_assignment_is_variable_binding_statement():
    scope = parse_scad("var1 = size/3;")
    assert len(scope.children) == 1
    binding = scope.children[0]
    assert isinstance(binding, VariableBindingStatement)
    assert binding.name == "var1"
    # Constant parts of the right-hand side are folded at construction.
    assert binding.value == BinaryOp("/", Variable("size"), NumberLiteral(3.0))


def test_assignment_inside_block_scopes_to_enclosing_scope():
    # A bare block is transparent, so `local` binds in the top-level scope.
    scope = parse_scad("{ local = 7; cube(local); }")
    assert [type(s).__name__ for s in scope.children] == [
        "VariableBindingStatement",
        "ModuleCallStatement",
    ]
    binding = scope.children[0]
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
    scope = parse_scad("cube(10+size);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "+"
    assert expr.left == NumberLiteral(10.0)
    assert expr.right == Variable("size")


def test_multiplicative_expression():
    scope = parse_scad("cube(10*size);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "*"
    assert expr.left == NumberLiteral(10.0)
    assert expr.right == Variable("size")


def test_paren_expression():
    scope = parse_scad("cube((size+20)/3);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "/"
    assert isinstance(expr.left, Paren)
    assert isinstance(expr.left.inner, BinaryOp)
    assert expr.left.inner.op == "+"


def test_array_literal_builds_list_of_expressions():
    scope = parse_scad("cube([12, var2+2, -3.2]);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, VectorLiteral)
    assert expr.elements == [
        NumberLiteral(12.0),
        BinaryOp("+", Variable("var2"), NumberLiteral(2.0)),
        NumberLiteral(-3.2),
    ]


def test_empty_array_literal():
    scope = parse_scad("cube([]);")
    assert single_call(scope).positional_args == [Literal([])]


## =========================================================================
#  Constant folding at construction


def test_constant_expression_folds_to_number_literal():
    scope = parse_scad("cube((10+20)/3);")
    assert single_call(scope).positional_args == [NumberLiteral(10.0)]


def test_constant_array_folds_to_literal():
    scope = parse_scad("cube([1, 2*3, -4]);")
    assert single_call(scope).positional_args == [Literal([1.0, 6.0, -4.0])]


def test_comments_are_ignored():
    scope = parse_scad("// line comment\ncube(1);\n/* block\ncomment */\nsphere(2);\n")
    assert call_names(scope.children) == ["cube", "sphere"]


## =========================================================================
#  Expression forms (the full operator/literal grammar)


def _binding_value(source: str):
    scope = parse_scad(source)
    binding = scope.children[0]
    assert isinstance(binding, VariableBindingStatement)
    return binding.value


def test_unary_minus_binds_looser_than_exponent():
    # OpenSCAD: -2^2 == -(2^2) == -4, so the sign is an expression node,
    # not part of the number token.
    scope = parse_scad("cube(-2^2);")
    assert single_call(scope).positional_args == [NumberLiteral(-4.0)]


def test_exponent_is_right_associative():
    scope = parse_scad("cube(2^3^2);")  # 2^(3^2) == 512
    assert single_call(scope).positional_args == [NumberLiteral(512.0)]


def test_precedence_multiplication_before_addition():
    scope = parse_scad("cube(1+2*3);")
    assert single_call(scope).positional_args == [NumberLiteral(7.0)]


def test_precedence_relational_binds_tighter_than_equality():
    scope = parse_scad("cube(1<2 == 3<4);")
    assert single_call(scope).positional_args == [BooleanLiteral(True)]


def test_logical_not_binds_tighter_than_and():
    scope = parse_scad("cube(!a && b);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, BinaryOp)
    assert expr.op == "&&"
    assert expr.left == UnaryOp("!", Variable("a"))
    assert expr.right == Variable("b")


def test_ternary_is_right_associative():
    scope = parse_scad("cube(a ? b : c ? d : e);")
    expr = single_call(scope).positional_args[0]
    assert isinstance(expr, TernaryOp)
    assert expr.then_expr == Variable("b")
    assert isinstance(expr.else_expr, TernaryOp)


def test_scientific_number_notation():
    assert single_call(parse_scad("cube(1e3);")).positional_args == [NumberLiteral(1000.0)]
    assert single_call(parse_scad("cube(2.5e-2);")).positional_args == [NumberLiteral(0.025)]


def test_string_literal_decodes_escapes():
    assert _binding_value('s = "a\\tb\\x41\\u03a9";') == StringLiteral("a\tbAΩ")


def test_range_literals():
    assert _binding_value("r = [3:5];") == Literal(RangeValue(3.0, 1.0, 5.0))
    assert _binding_value("r = [0:2:10];") == Literal(RangeValue(0.0, 2.0, 10.0))


def test_index_expression_folds_constants():
    assert _binding_value("v = [1,2,3][1];") == Literal(2.0)
    assert _binding_value('s = "abc"[2];') == StringLiteral("c")


def test_member_access_is_index_sugar():
    assert _binding_value("p = [1,2,3].y;") == Literal(2.0)


def test_member_access_unknown_member_is_syntax_error():
    with pytest.raises(ProtoSCADError) as excinfo:
        parse_scad("p = [1,2].q;")
    assert excinfo.value.diagnostic.code == ErrorCode.SYNTAX


def test_function_call_expression():
    assert _binding_value("x = sin(90) + 1;") == BinaryOp("+", Call("sin", [NumberLiteral(90.0)]), NumberLiteral(1.0))


def test_let_expression():
    assert _binding_value("x = let(a=2) a*3;") == LetExpr(
        [Assignment("a", NumberLiteral(2.0))],
        BinaryOp("*", Variable("a"), NumberLiteral(3.0)),
    )


def test_undef_and_boolean_literals_parse():
    assert _binding_value("u = undef;") == UndefLiteral()
    assert _binding_value("b = true;") == BooleanLiteral(True)


## =========================================================================
#  Syntax rejection


def test_named_arg_before_positional_is_rejected():
    _, errors = parse_scad_with_errors("foo(bar=2, 1);")
    assert errors, "expected a syntax error for named-before-positional args"


def test_valid_mixed_args_produce_no_errors():
    _, errors = parse_scad_with_errors("foo(1, 2, r=5);")
    assert errors == []


def test_logical_or_expression():
    expr = _binding_value("x = a || b;")
    assert expr == BinaryOp("||", Variable("a"), Variable("b"))


def test_function_call_rejects_named_arguments():
    with pytest.raises(ProtoSCADError) as excinfo:
        parse_scad("x = pow(2, e=3);")
    assert excinfo.value.diagnostic.code == ErrorCode.INVALID_ARGUMENT


def test_let_expression_folds_constant_body():
    expr = _binding_value("x = let(a=2) 3+4;")
    assert isinstance(expr, LetExpr)
    assert expr.body == NumberLiteral(7.0)


## =========================================================================
#  if / else statements


def test_if_without_else():
    (if_call,) = parse_scad("if (x > 1) cube(2);").children
    assert isinstance(if_call, ModuleCallStatement)
    assert if_call.module == "if"
    assert if_call.positional_args == [BinaryOp(">", Variable("x"), NumberLiteral(1.0))]
    assert if_call.named_args == {}
    # One child: the true branch as an implicit-union scope.
    (then_scope,) = if_call.children
    assert then_scope.module == "union"
    (then_call,) = then_scope.children
    assert then_call.module == "cube"
    assert then_call.positional_args == [NumberLiteral(2.0)]


def test_if_else():
    (if_call,) = parse_scad("if (x) cube(1); else sphere(2);").children
    # Two children: the true branch, then the false branch.
    assert [child.module for child in if_call.children] == ["union", "union"]
    (then_call,) = if_call.children[0].children
    (else_call,) = if_call.children[1].children
    assert then_call.module == "cube"
    assert else_call.module == "sphere"
    assert else_call.positional_args == [NumberLiteral(2.0)]


def test_if_with_block_body_and_empty_else_block():
    (if_call,) = parse_scad("if (x) { cube(1); sphere(2); } else { }").children
    then_scope, else_scope = if_call.children
    assert [child.module for child in then_scope.children] == ["cube", "sphere"]
    assert else_scope.children == []


def test_if_branches_are_never_more_than_two_and_never_shift():
    # The branch positions are fixed: an empty branch is an empty union
    # scope, so index 0 is always the true branch and index 1 the false one.
    (if_call,) = parse_scad("if (x) ; else cube(1);").children
    assert len(if_call.children) == 2
    assert if_call.children[0].children == []
    (else_call,) = if_call.children[1].children
    assert else_call.module == "cube"


def test_if_else_if_chain_nests_in_else_position():
    (outer,) = parse_scad("if (a) cube(1); else if (b) sphere(2); else cylinder(3);").children
    assert outer.module == "if"
    assert len(outer.children) == 2
    (middle,) = outer.children[1].children
    assert middle.module == "if"
    assert middle.positional_args == [Variable("b")]
    (final,) = middle.children[1].children
    assert final.module == "cylinder"


def test_then_branch_can_be_a_nested_if():
    (outer,) = parse_scad("if (a) if (b) cube(1);").children
    assert len(outer.children) == 1
    (inner,) = outer.children[0].children
    assert inner.module == "if"


def test_dangling_else_binds_to_innermost_if():
    (outer,) = parse_scad("if (a) if (b) cube(1); else cube(2);").children
    assert len(outer.children) == 1
    (inner,) = outer.children[0].children
    assert inner.module == "if"
    (inner_else,) = inner.children[1].children
    assert inner_else.module == "cube"


def test_if_in_module_call_chain_terminates_the_chain():
    # The sphere is a sibling statement, not a conditional child of the if.
    (translate_call, sphere_call) = parse_scad("translate([1,0,0]) if (x) cube(1); sphere(2);").children
    assert translate_call.module == "translate"
    (if_call,) = translate_call.children
    assert if_call.module == "if"
    assert sphere_call.module == "sphere"


def test_if_is_a_statement_inside_blocks_and_module_bodies():
    module_src = "module m() if (x) cube(1);"
    (definition,) = parse_scad(module_src).children
    assert isinstance(definition, ModuleDefinitionStatement)
    (if_call,) = definition.body.children
    assert if_call.module == "if"

    (block_if,) = parse_scad("{ if (x) cube(1); }").children
    assert block_if.module == "if"


def test_if_with_empty_branches():
    (if_call,) = parse_scad("if (x) ; else ;").children
    assert [child.module for child in if_call.children] == ["union", "union"]
    assert all(child.children == [] for child in if_call.children)


def test_if_and_else_are_reserved_but_prefix_names_are_not():
    # Longer names that merely start with a keyword still lex as identifiers.
    scope = parse_scad("iffy = 3; elsewise = 4;")
    assert [(binding.name, binding.value) for binding in scope.children] == [
        ("iffy", NumberLiteral(3.0)),
        ("elsewise", NumberLiteral(4.0)),
    ]
