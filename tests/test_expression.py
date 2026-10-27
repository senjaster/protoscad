from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from protoscad.diagnostics import ProtoSCADError
from protoscad.runtime.environment import Environment
from protoscad.tree.expression import (
    ArrayLiteral,
    Assignment,
    BinaryOp,
    Expression,
    Literal,
    NumberLiteral,
    Paren,
    Raw,
    Variable,
    fold,
)


@pytest.fixture
def env() -> Environment:
    return Environment()


def make_env(**variables: float) -> Environment:
    return Environment(variables={name: Assignment(name, NumberLiteral(value)) for name, value in variables.items()})


def test_expression_base_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        Expression().evaluate(Environment())


def test_number_literal_returns_value():
    assert NumberLiteral(3.5).evaluate(Environment()) == 3.5
    assert NumberLiteral(-2.0).evaluate(Environment()) == -2.0


def test_variable_resolves_through_environment():
    env = make_env(x=42.0)
    assert Variable("x").evaluate(env) == 42.0


def test_variable_missing_returns_none():
    assert Variable("nope").evaluate(Environment()) is None


@pytest.mark.parametrize(
    "op,left,right,expected",
    [
        ("+", 10.0, 5.0, 15.0),
        ("-", 10.0, 5.0, 5.0),
        ("*", 10.0, 5.0, 50.0),
        ("/", 10.0, 5.0, 2.0),
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


def test_binary_op_unknown_operator_raises_at_construction():
    # Operators come from the grammar, so an unknown one is a construction
    # bug and fails fast in __post_init__, not at evaluation.
    with pytest.raises(ProtoSCADError, match="Unknown binary operator"):
        BinaryOp("^", NumberLiteral(2.0), NumberLiteral(3.0))


def test_paren_delegates_to_inner():
    inner = BinaryOp("+", NumberLiteral(1.0), NumberLiteral(2.0))
    assert Paren(inner).evaluate(Environment()) == 3.0


def test_raw_returns_text():
    assert Raw("[1, 2, 3]").evaluate(Environment()) == "[1, 2, 3]"


def test_array_literal_evaluates_elements():
    expr = ArrayLiteral(
        [
            NumberLiteral(1.0),
            BinaryOp("+", NumberLiteral(2.0), NumberLiteral(3.0)),
        ]
    )
    assert expr.evaluate(Environment()) == [1.0, 5.0]


def test_array_literal_empty():
    assert ArrayLiteral([]).evaluate(Environment()) == []


def test_assignment_is_plain_data():
    # Assignment is no longer an Expression: it records a binding without
    # scoping behaviour of its own.
    assignment = Assignment("x", NumberLiteral(1.0))
    assert assignment.name == "x"
    assert assignment.value == NumberLiteral(1.0)
    assert not isinstance(assignment, Expression)


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


def test_fold_leaves_variables_in_place():
    expr = BinaryOp("+", Variable("x"), NumberLiteral(1.0))
    assert fold(expr) == expr


def test_fold_drops_paren_around_constant():
    assert fold(Paren(BinaryOp("+", NumberLiteral(1.0), NumberLiteral(2.0)))) == NumberLiteral(3.0)


def test_fold_keeps_paren_around_variables():
    inner = BinaryOp("+", Variable("x"), NumberLiteral(2.0))
    assert fold(Paren(inner)) == Paren(inner)


def test_fold_array_of_constants_becomes_literal():
    expr = ArrayLiteral([NumberLiteral(1.0), BinaryOp("*", NumberLiteral(2.0), NumberLiteral(3.0))])
    assert fold(expr) == Literal([1.0, 6.0])


def test_fold_array_with_variable_stays_array():
    expr = ArrayLiteral([NumberLiteral(1.0), Variable("x")])
    assert fold(expr) == ArrayLiteral([NumberLiteral(1.0), Variable("x")])


def test_fold_empty_array_becomes_literal():
    assert fold(ArrayLiteral([])) == Literal([])


def test_fold_skips_operations_that_would_raise():
    expr = BinaryOp("/", NumberLiteral(1.0), NumberLiteral(0.0))
    assert fold(expr) == expr
    # Left unfolded, the error surfaces at evaluation, in context.
    with pytest.raises(ZeroDivisionError):
        expr.evaluate(Environment())


## =========================================================================
#  referenced_names


def test_referenced_names_collects_variables_from_nested_children():
    expr = BinaryOp("+", Variable("x"), ArrayLiteral([NumberLiteral(1.0), Variable("a"), Variable("x")]))
    assert expr.referenced_names() == {"x", "a"}


def test_referenced_names_empty_for_constants():
    assert NumberLiteral(1.0).referenced_names() == set()
    assert Raw("text").referenced_names() == set()
    assert Paren(BinaryOp("*", NumberLiteral(2.0), NumberLiteral(3.0))).referenced_names() == set()


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
