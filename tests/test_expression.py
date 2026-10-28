from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import pytest

from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.runtime.environment import Environment
from protoscad.tree.expression import (
    Assignment,
    BinaryOp,
    BooleanLiteral,
    Call,
    Expression,
    Index,
    LetExpr,
    Literal,
    NumberLiteral,
    Paren,
    RangeLiteral,
    StringLiteral,
    TernaryOp,
    UnaryOp,
    UndefLiteral,
    Variable,
    VectorLiteral,
    fold,
)
from protoscad.tree.values import (
    RangeValue,
    Type,
    format_value,
    ieee_div,
    type_of,
    unescape_string,
)


@pytest.fixture
def env() -> Environment:
    return Environment()


def make_env(**variables: float) -> Environment:
    return Environment(variables={name: Assignment(name, NumberLiteral(value)) for name, value in variables.items()})


@dataclass
class Exploding(Expression):
    """Test double that fails the test if it is ever evaluated — for
    proving that only the taken branch of a lazy construct runs."""

    def evaluate(self, env: Environment) -> Any:
        raise AssertionError("expression must not be evaluated")


## =========================================================================
#  Literals


def test_expression_base_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        Expression().evaluate(Environment())


def test_number_literal_returns_value():
    assert NumberLiteral(3.5).evaluate(Environment()) == 3.5
    assert NumberLiteral(-2.0).evaluate(Environment()) == -2.0


def test_string_literal_returns_value():
    assert StringLiteral("hello").evaluate(Environment()) == "hello"


def test_boolean_literals():
    assert BooleanLiteral(True).evaluate(Environment()) is True
    assert BooleanLiteral(False).evaluate(Environment()) is False


def test_undef_literal_evaluates_to_none():
    value = UndefLiteral().evaluate(Environment())
    assert value is None


def test_variable_resolves_through_environment():
    env = make_env(x=42.0)
    assert Variable("x").evaluate(env) == 42.0


def test_variable_missing_returns_none():
    assert Variable("nope").evaluate(Environment()) is None


def test_assignment_is_plain_data():
    assignment = Assignment("x", NumberLiteral(1.0))
    assert assignment.name == "x"
    assert assignment.value == NumberLiteral(1.0)
    assert not isinstance(assignment, Expression)


## =========================================================================
#  Unary operators


def test_unary_minus_negates_number():
    assert UnaryOp("-", NumberLiteral(2.0)).evaluate(Environment()) == -2.0


def test_unary_minus_negates_vector_elementwise():
    expr = UnaryOp("-", VectorLiteral([NumberLiteral(1.0), NumberLiteral(2.0)]))
    assert expr.evaluate(Environment()) == [-1.0, -2.0]


def test_unary_minus_rejects_string():
    with pytest.raises(ProtoSCADError) as excinfo:
        UnaryOp("-", StringLiteral("a")).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.TYPE_ERROR


def test_unary_plus_is_identity_on_numbers():
    assert UnaryOp("+", NumberLiteral(2.0)).evaluate(Environment()) == 2.0


def test_logical_not_uses_openscad_truthiness():
    assert UnaryOp("!", NumberLiteral(0.0)).evaluate(Environment()) is True
    assert UnaryOp("!", NumberLiteral(1.0)).evaluate(Environment()) is False
    assert UnaryOp("!", StringLiteral("")).evaluate(Environment()) is True
    assert UnaryOp("!", VectorLiteral([])).evaluate(Environment()) is True
    # nan is truthy in OpenSCAD, so !nan is false
    assert UnaryOp("!", Literal(math.nan)).evaluate(Environment()) is False


def test_unary_unknown_operator_raises_at_construction():
    with pytest.raises(ProtoSCADError, match="Unknown unary operator"):
        UnaryOp("~", NumberLiteral(1.0))


## =========================================================================
#  Binary operators: scalar arithmetic (IEEE-754, like OpenSCAD doubles)


@pytest.mark.parametrize(
    "op,left,right,expected",
    [
        ("+", 10.0, 5.0, 15.0),
        ("-", 10.0, 5.0, 5.0),
        ("*", 10.0, 5.0, 50.0),
        ("/", 10.0, 5.0, 2.0),
        ("%", 10.0, 3.0, 1.0),
        ("^", 2.0, 10.0, 1024.0),
    ],
)
def test_binary_op_arithmetic(op, left, right, expected):
    expr = BinaryOp(op, NumberLiteral(left), NumberLiteral(right))
    assert expr.evaluate(Environment()) == expected


def test_binary_op_nested():
    # (10 + 20) / 3
    expr = BinaryOp(
        "/",
        BinaryOp("+", NumberLiteral(10.0), NumberLiteral(20.0)),
        NumberLiteral(3.0),
    )
    assert expr.evaluate(Environment()) == 10.0


def test_division_by_zero_is_inf_not_an_error():
    assert BinaryOp("/", NumberLiteral(1.0), NumberLiteral(0.0)).evaluate(Environment()) == math.inf
    assert BinaryOp("/", NumberLiteral(1.0), NumberLiteral(-0.0)).evaluate(Environment()) == -math.inf
    assert math.isnan(BinaryOp("/", NumberLiteral(0.0), NumberLiteral(0.0)).evaluate(Environment()))


def test_modulo_keeps_dividend_sign_and_nan_on_zero():
    assert BinaryOp("%", NumberLiteral(10.0), NumberLiteral(3.0)).evaluate(Environment()) == 1.0
    assert BinaryOp("%", NumberLiteral(-10.0), NumberLiteral(3.0)).evaluate(Environment()) == -1.0
    assert math.isnan(BinaryOp("%", NumberLiteral(1.0), NumberLiteral(0.0)).evaluate(Environment()))


def test_power_handles_domain_errors():
    assert math.isnan(BinaryOp("^", NumberLiteral(-8.0), NumberLiteral(0.5)).evaluate(Environment()))
    assert BinaryOp("^", NumberLiteral(0.0), NumberLiteral(-1.0)).evaluate(Environment()) == math.inf


def test_binary_op_unknown_operator_raises_at_construction():
    # Operators come from the grammar, so an unknown one is a construction
    # bug and fails fast in __post_init__, not at evaluation.
    with pytest.raises(ProtoSCADError, match="Unknown binary operator"):
        BinaryOp("&", NumberLiteral(2.0), NumberLiteral(3.0))


def test_type_mismatch_raises_type_error_with_operator_and_types():
    with pytest.raises(ProtoSCADError) as excinfo:
        BinaryOp("+", NumberLiteral(1.0), StringLiteral("a")).evaluate(Environment())
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.TYPE_ERROR
    assert "number" in diagnostic.message and "string" in diagnostic.message


## =========================================================================
#  Binary operators: vectors and matrices


def vec(*values: float) -> VectorLiteral:
    return VectorLiteral([NumberLiteral(value) for value in values])


def test_vector_addition_is_elementwise():
    expr = BinaryOp("+", vec(1.0, 2.0, 3.0), vec(10.0, 20.0, 30.0))
    assert expr.evaluate(Environment()) == [11.0, 22.0, 33.0]


def test_vector_addition_truncates_to_shorter():
    expr = BinaryOp("+", vec(1.0, 2.0), vec(10.0, 20.0, 30.0))
    assert expr.evaluate(Environment()) == [11.0, 22.0]


def test_vector_pairwise_type_mismatch_becomes_undef_element():
    expr = BinaryOp("+", VectorLiteral([NumberLiteral(1.0)]), VectorLiteral([StringLiteral("a")]))
    assert expr.evaluate(Environment()) == [None]


def test_vector_scalar_multiplication_and_division():
    assert BinaryOp("*", NumberLiteral(2.0), vec(1.0, 2.0)).evaluate(Environment()) == [2.0, 4.0]
    assert BinaryOp("/", vec(1.0, 2.0), NumberLiteral(2.0)).evaluate(Environment()) == [0.5, 1.0]


def test_scalar_multiplication_recurses_into_nesting():
    expr = BinaryOp("*", NumberLiteral(2.0), VectorLiteral([NumberLiteral(1.0), vec(2.0)]))
    assert expr.evaluate(Environment()) == [2.0, [4.0]]


def test_vector_dot_product():
    assert BinaryOp("*", vec(1.0, 2.0, 3.0), vec(4.0, 5.0, 6.0)).evaluate(Environment()) == 32.0


def test_vector_dot_product_length_mismatch_raises():
    with pytest.raises(ProtoSCADError) as excinfo:
        BinaryOp("*", vec(1.0), vec(1.0, 2.0)).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.TYPE_ERROR


def test_matrix_vector_product():
    matrix = VectorLiteral([vec(1.0, 2.0), vec(3.0, 4.0)])
    assert BinaryOp("*", matrix, vec(5.0, 6.0)).evaluate(Environment()) == [17.0, 39.0]
    assert BinaryOp("*", vec(1.0, 0.0), matrix).evaluate(Environment()) == [1.0, 2.0]


def test_matrix_matrix_product():
    matrix = VectorLiteral([vec(1.0, 2.0), vec(3.0, 4.0)])
    identity = VectorLiteral([vec(1.0, 0.0), vec(0.0, 1.0)])
    assert BinaryOp("*", matrix, identity).evaluate(Environment()) == [[1.0, 2.0], [3.0, 4.0]]


def test_vector_plus_scalar_raises():
    with pytest.raises(ProtoSCADError) as excinfo:
        BinaryOp("+", vec(1.0), NumberLiteral(2.0)).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.TYPE_ERROR


## =========================================================================
#  Comparisons, equality, logic


def test_number_comparisons():
    assert BinaryOp("<", NumberLiteral(1.0), NumberLiteral(2.0)).evaluate(Environment()) is True
    assert BinaryOp(">=", NumberLiteral(2.0), NumberLiteral(2.0)).evaluate(Environment()) is True


def test_string_comparison_is_alphabetical():
    assert BinaryOp(">", StringLiteral("ab"), StringLiteral("aa")).evaluate(Environment()) is True


def test_boolean_coerces_to_number_in_comparisons():
    assert BinaryOp(">", BooleanLiteral(True), NumberLiteral(0.5)).evaluate(Environment()) is True
    assert BinaryOp("<", BooleanLiteral(False), BooleanLiteral(True)).evaluate(Environment()) is True


def test_mixed_type_ordering_raises():
    with pytest.raises(ProtoSCADError) as excinfo:
        BinaryOp("<", NumberLiteral(1.0), StringLiteral("a")).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.TYPE_ERROR


def test_nan_orders_false():
    nan = Literal(math.nan)
    assert BinaryOp("<", nan, NumberLiteral(1.0)).evaluate(Environment()) is False
    assert BinaryOp("==", nan, nan).evaluate(Environment()) is False


def test_equality_is_deep_and_type_aware():
    assert BinaryOp("==", vec(1.0, 2.0), vec(1.0, 2.0)).evaluate(Environment()) is True
    assert BinaryOp("==", NumberLiteral(1.0), StringLiteral("1")).evaluate(Environment()) is False
    assert BinaryOp("==", UndefLiteral(), UndefLiteral()).evaluate(Environment()) is True
    assert BinaryOp("==", BooleanLiteral(True), NumberLiteral(1.0)).evaluate(Environment()) is True
    assert BinaryOp("!=", NumberLiteral(1.0), NumberLiteral(2.0)).evaluate(Environment()) is True


def test_logical_operators_use_truthiness():
    assert BinaryOp("&&", NumberLiteral(0.0), NumberLiteral(1.0)).evaluate(Environment()) is False
    assert BinaryOp("&&", NumberLiteral(2.0), StringLiteral("x")).evaluate(Environment()) is True
    assert BinaryOp("||", VectorLiteral([]), StringLiteral("")).evaluate(Environment()) is False
    assert BinaryOp("||", VectorLiteral([]), NumberLiteral(1.0)).evaluate(Environment()) is True


def test_logical_operators_short_circuit():
    assert BinaryOp("&&", BooleanLiteral(False), Exploding()).evaluate(Environment()) is False
    assert BinaryOp("||", BooleanLiteral(True), Exploding()).evaluate(Environment()) is True


def test_paren_delegates_to_inner():
    inner = BinaryOp("+", NumberLiteral(1.0), NumberLiteral(2.0))
    assert Paren(inner).evaluate(Environment()) == 3.0


## =========================================================================
#  Ternary, index, ranges


def test_ternary_picks_branch_by_truthiness():
    expr = TernaryOp(NumberLiteral(0.0), NumberLiteral(1.0), NumberLiteral(2.0))
    assert expr.evaluate(Environment()) == 2.0  # 0 is falsy in OpenSCAD


def test_ternary_evaluates_only_taken_branch():
    expr = TernaryOp(BooleanLiteral(False), Exploding(), NumberLiteral(7.0))
    assert expr.evaluate(Environment()) == 7.0


def test_index_reads_vector_and_string():
    assert Index(Literal([10.0, 20.0, 30.0]), NumberLiteral(1.0)).evaluate(Environment()) == 20.0
    assert Index(StringLiteral("abc"), NumberLiteral(1.0)).evaluate(Environment()) == "b"


def test_index_out_of_range_raises():
    with pytest.raises(ProtoSCADError) as excinfo:
        Index(Literal([1.0]), NumberLiteral(5.0)).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.INDEX_OUT_OF_RANGE


def test_index_must_be_integer_number():
    with pytest.raises(ProtoSCADError) as excinfo:
        Index(Literal([1.0]), NumberLiteral(1.5)).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.INVALID_INDEX
    with pytest.raises(ProtoSCADError):
        Index(Literal([1.0]), StringLiteral("a")).evaluate(Environment())


def test_indexing_scalar_raises():
    with pytest.raises(ProtoSCADError) as excinfo:
        Index(NumberLiteral(1.0), NumberLiteral(0.0)).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.TYPE_ERROR


def test_range_literal_evaluates_to_range_value():
    expr = RangeLiteral(NumberLiteral(0.0), NumberLiteral(2.0), NumberLiteral(10.0))
    assert expr.evaluate(Environment()) == RangeValue(0.0, 2.0, 10.0)


def test_range_literal_without_step_defaults_to_one():
    expr = RangeLiteral(NumberLiteral(3.0), None, NumberLiteral(5.0))
    assert expr.evaluate(Environment()) == RangeValue(3.0, 1.0, 5.0)


def test_range_literal_non_numeric_bounds_raise():
    with pytest.raises(ProtoSCADError) as excinfo:
        RangeLiteral(StringLiteral("a"), None, NumberLiteral(5.0)).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.TYPE_ERROR


## =========================================================================
#  Calls and let


def test_call_invokes_builtin_function():
    assert Call("sin", [NumberLiteral(90.0)]).evaluate(Environment()) == pytest.approx(1.0)
    assert Call("len", [Literal([1.0, 2.0, 3.0])]).evaluate(Environment()) == 3.0


def test_call_unknown_function_raises():
    with pytest.raises(ProtoSCADError) as excinfo:
        Call("frobnicate", []).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.UNKNOWN_FUNCTION


def test_call_type_mismatch_raises_invalid_argument():
    with pytest.raises(ProtoSCADError) as excinfo:
        Call("sin", [StringLiteral("a")]).evaluate(Environment())
    assert excinfo.value.diagnostic.code == ErrorCode.INVALID_ARGUMENT


def test_let_expr_binds_scope_for_body():
    body = BinaryOp("*", Variable("a"), NumberLiteral(3.0))
    expr = LetExpr([Assignment("a", NumberLiteral(2.0))], body)
    assert expr.evaluate(Environment()) == 6.0


def test_let_expr_binding_sees_parent_scope():
    expr = LetExpr(
        [Assignment("a", BinaryOp("+", Variable("b"), NumberLiteral(1.0)))],
        Variable("a"),
    )
    assert expr.evaluate(make_env(b=10.0)) == 11.0


## =========================================================================
#  expression_type


def test_expression_type_of_literals():
    assert NumberLiteral(1.0).expression_type is Type.NUMBER
    assert StringLiteral("a").expression_type is Type.STRING
    assert BooleanLiteral(True).expression_type is Type.BOOLEAN
    assert UndefLiteral().expression_type is Type.UNDEF
    assert VectorLiteral([]).expression_type is Type.VECTOR
    assert RangeLiteral(NumberLiteral(0.0), None, NumberLiteral(1.0)).expression_type is Type.RANGE
    assert Literal("x").expression_type is Type.STRING


def test_expression_type_of_composites():
    assert BinaryOp("+", NumberLiteral(1.0), NumberLiteral(2.0)).expression_type is Type.NUMBER
    assert BinaryOp("+", vec(1.0), vec(2.0)).expression_type is Type.VECTOR
    assert BinaryOp("*", NumberLiteral(2.0), vec(1.0)).expression_type is Type.VECTOR
    assert BinaryOp("/", vec(1.0), NumberLiteral(2.0)).expression_type is Type.VECTOR
    assert BinaryOp("<", NumberLiteral(1.0), NumberLiteral(2.0)).expression_type is Type.BOOLEAN
    assert BinaryOp("&&", BooleanLiteral(True), BooleanLiteral(False)).expression_type is Type.BOOLEAN
    assert UnaryOp("-", NumberLiteral(1.0)).expression_type is Type.NUMBER
    assert UnaryOp("!", Variable("a")).expression_type is Type.BOOLEAN


def test_expression_type_unknown_when_dynamic():
    assert Variable("x").expression_type is Type.UNKNOWN
    assert BinaryOp("+", Variable("x"), NumberLiteral(1.0)).expression_type is Type.UNKNOWN
    assert Index(Literal([1.0]), NumberLiteral(0.0)).expression_type is Type.UNKNOWN
    assert Index(StringLiteral("abc"), NumberLiteral(0.0)).expression_type is Type.STRING
    assert TernaryOp(Variable("c"), NumberLiteral(1.0), NumberLiteral(2.0)).expression_type is Type.NUMBER
    assert TernaryOp(Variable("c"), NumberLiteral(1.0), StringLiteral("a")).expression_type is Type.UNKNOWN
    assert Paren(Variable("x")).expression_type is Type.UNKNOWN
    body = BinaryOp("+", Variable("a"), NumberLiteral(1.0))
    assert LetExpr([Assignment("a", NumberLiteral(1.0))], body).expression_type is Type.UNKNOWN


## =========================================================================
#  Constant folding


def test_fold_collapses_constant_arithmetic():
    # (10 + 20) / 3
    expr = BinaryOp("/", Paren(BinaryOp("+", NumberLiteral(10.0), NumberLiteral(20.0))), NumberLiteral(3.0))
    assert fold(expr) == NumberLiteral(10.0)


def test_fold_keeps_number_literals_typed():
    assert fold(BinaryOp("*", NumberLiteral(2.0), NumberLiteral(3.0))) == NumberLiteral(6.0)


def test_fold_mixed_constants_become_literal():
    assert fold(BinaryOp("+", NumberLiteral(1.0), Literal(2.0))) == Literal(3.0)


def test_fold_division_by_zero_folds_to_inf():
    # OpenSCAD numbers are IEEE doubles: 1/0 is inf, not an error.
    expr = BinaryOp("/", NumberLiteral(1.0), NumberLiteral(0.0))
    assert fold(expr) == NumberLiteral(math.inf)


def test_fold_type_error_left_unfolded():
    expr = BinaryOp("+", NumberLiteral(1.0), StringLiteral("a"))
    assert fold(expr) == expr
    # Left unfolded, the error surfaces at evaluation, in context.
    with pytest.raises(ProtoSCADError):
        expr.evaluate(Environment())


def test_fold_unary_minus_of_constant():
    assert fold(UnaryOp("-", NumberLiteral(5.0))) == NumberLiteral(-5.0)
    assert fold(UnaryOp("-", Literal([1.0, 2.0]))) == Literal([-1.0, -2.0])
    assert fold(UnaryOp("+", NumberLiteral(5.0))) == NumberLiteral(5.0)


def test_fold_logical_not():
    assert fold(UnaryOp("!", BooleanLiteral(False))) == BooleanLiteral(True)
    assert fold(UnaryOp("!", NumberLiteral(0.0))) == BooleanLiteral(True)


def test_fold_comparison_produces_boolean_literal():
    assert fold(BinaryOp("<", NumberLiteral(1.0), NumberLiteral(2.0))) == BooleanLiteral(True)
    assert fold(BinaryOp("==", vec(1.0), vec(1.0))) == BooleanLiteral(True)


def test_fold_constant_ternary_takes_only_one_branch():
    expr = TernaryOp(BooleanLiteral(False), NumberLiteral(1.0), BinaryOp("*", NumberLiteral(2.0), NumberLiteral(3.0)))
    assert fold(expr) == NumberLiteral(6.0)
    # The untaken branch is not even folded into a constant.
    exploded = TernaryOp(BooleanLiteral(True), NumberLiteral(1.0), Exploding())
    assert fold(exploded) == NumberLiteral(1.0)


def test_fold_keeps_ternary_with_dynamic_condition():
    inner = TernaryOp(Variable("c"), NumberLiteral(1.0), NumberLiteral(2.0))
    assert fold(inner) == TernaryOp(Variable("c"), NumberLiteral(1.0), NumberLiteral(2.0))


def test_fold_constant_index():
    assert fold(Index(Literal([10.0, 20.0]), NumberLiteral(1.0))) == Literal(20.0)
    assert fold(Index(StringLiteral("abc"), NumberLiteral(1.0))) == StringLiteral("b")
    out_of_range = Index(Literal([1.0]), NumberLiteral(3.0))
    assert fold(out_of_range) == out_of_range


def test_fold_constant_range():
    expr = RangeLiteral(NumberLiteral(0.0), None, NumberLiteral(5.0))
    assert fold(expr) == Literal(RangeValue(0.0, 1.0, 5.0))


def test_fold_leaves_variables_in_place():
    expr = BinaryOp("+", Variable("x"), NumberLiteral(1.0))
    assert fold(expr) == expr


def test_fold_drops_paren_around_constant():
    assert fold(Paren(BinaryOp("+", NumberLiteral(1.0), NumberLiteral(2.0)))) == NumberLiteral(3.0)


def test_fold_keeps_paren_around_variables():
    inner = BinaryOp("+", Variable("x"), NumberLiteral(2.0))
    assert fold(Paren(inner)) == Paren(inner)


def test_fold_array_of_constants_becomes_literal():
    expr = VectorLiteral([NumberLiteral(1.0), BinaryOp("*", NumberLiteral(2.0), NumberLiteral(3.0))])
    assert fold(expr) == Literal([1.0, 6.0])


def test_fold_array_with_variable_stays_array():
    expr = VectorLiteral([NumberLiteral(1.0), Variable("x")])
    assert fold(expr) == VectorLiteral([NumberLiteral(1.0), Variable("x")])


def test_fold_empty_array_becomes_literal():
    assert fold(VectorLiteral([])) == Literal([])


## =========================================================================
#  referenced_names


def test_referenced_names_collects_variables_from_nested_children():
    expr = BinaryOp("+", Variable("x"), VectorLiteral([NumberLiteral(1.0), Variable("a"), Variable("x")]))
    assert expr.referenced_names() == {"x", "a"}


def test_referenced_names_empty_for_constants():
    assert NumberLiteral(1.0).referenced_names() == set()
    assert StringLiteral("text").referenced_names() == set()
    assert Paren(BinaryOp("*", NumberLiteral(2.0), NumberLiteral(3.0))).referenced_names() == set()


def test_referenced_names_sees_let_bindings_and_call_args():
    expr = LetExpr(
        [Assignment("a", BinaryOp("+", Variable("x"), NumberLiteral(1.0)))],
        Call("min", [Variable("a"), Variable("y")]),
    )
    # "a" is bound by the let but still *read* by the expression;
    # referenced_names reports reads, not free names.
    assert expr.referenced_names() == {"x", "y", "a"}
    assert Call("sin", [Variable("t")]).referenced_names() == {"t"}


def test_referenced_names_works_for_new_node_types():
    # Node types (and test doubles) declared after the fact participate
    # automatically: the base class walks dataclass fields.
    @dataclass
    class Pair(Expression):
        left: Expression
        right: Expression

        def evaluate(self, env: Environment) -> Any:
            raise NotImplementedError

    expr = Pair(Variable("p"), BinaryOp("+", Variable("q"), NumberLiteral(1.0)))
    assert expr.referenced_names() == {"p", "q"}


## =========================================================================
#  values helpers


def test_type_of_distinguishes_bool_from_number():
    assert type_of(True) is Type.BOOLEAN
    assert type_of(1.0) is Type.NUMBER
    assert type_of(None) is Type.UNDEF
    assert type_of([1.0]) is Type.VECTOR
    assert type_of("a") is Type.STRING
    assert type_of(RangeValue(0, 1, 1)) is Type.RANGE


def test_range_value_length_and_iteration():
    assert list(RangeValue(0.0, 1.0, 5.0)) == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]  # end inclusive
    assert list(RangeValue(0.0, 2.0, 5.0)) == [0.0, 2.0, 4.0]  # a never equals end
    assert list(RangeValue(3.0, -2.0, -1.0)) == [3.0, 1.0, -1.0]  # negative step
    assert list(RangeValue(0.0, 0.5, 5.0)) == [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    assert len(RangeValue(5.0, 1.0, 1.0)) == 0  # walks away from end
    with pytest.raises(ProtoSCADError):
        RangeValue(0.0, 0.0, 1.0)


def test_format_value_matches_openscad_printing():
    assert format_value(None) == "undef"
    assert format_value(True) == "true"
    assert format_value(False) == "false"
    assert format_value(1.0) == "1"
    assert format_value(1.5) == "1.5"
    assert format_value(math.inf) == "inf"
    assert format_value(math.nan) == "nan"
    assert format_value([1.0, "a", True]) == "[1, a, true]"
    assert format_value(RangeValue(0.0, 1.0, 5.0)) == "[0:5]"
    assert format_value(RangeValue(0.0, 2.0, 5.0)) == "[0:2:5]"


def test_unescape_string_decodes_all_escape_kinds():
    assert unescape_string(r"a\nb") == "a\nb"
    assert unescape_string(r"\t\\\"") == '\t\\"'
    assert unescape_string(r"\x41") == "A"
    assert unescape_string(r"\u03a9") == "Ω"
    assert unescape_string(r"\U01f600") == "😀"


@pytest.mark.parametrize("raw", [r"\q", r"\x4", r"\u12g4"])
def test_unescape_string_rejects_invalid_escapes(raw):
    with pytest.raises(ProtoSCADError):
        unescape_string(raw)


def test_ieee_div_signs():
    assert ieee_div(-1.0, 0.0) == -math.inf
    assert ieee_div(1.0, -0.0) == -math.inf
    assert math.isnan(ieee_div(-0.0, 0.0))
