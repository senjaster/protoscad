from __future__ import annotations

import pytest

from manifold_learn.ast.environment import Environment
from manifold_learn.ast.expression import (
    ArrayLiteral,
    BinaryOp,
    Expression,
    NumberLiteral,
    Paren,
    Raw,
    Variable,
    Assignment,
)


@pytest.fixture
def env() -> Environment:
    return Environment()


def make_env(**variables: float) -> Environment:
    return Environment(
        variables={name: Assignment(name, NumberLiteral(value)) for name, value in variables.items()}
    )


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


def test_binary_op_unknown_operator_raises():
    expr = BinaryOp("^", NumberLiteral(2.0), NumberLiteral(3.0))
    with pytest.raises(ValueError):
        expr.evaluate(Environment())


def test_paren_delegates_to_inner():
    inner = BinaryOp("+", NumberLiteral(1.0), NumberLiteral(2.0))
    assert Paren(inner).evaluate(Environment()) == 3.0


def test_raw_returns_text():
    assert Raw("[1, 2, 3]").evaluate(Environment()) == "[1, 2, 3]"


def test_array_literal_evaluates_elements():
    expr = ArrayLiteral([
        NumberLiteral(1.0),
        BinaryOp("+", NumberLiteral(2.0), NumberLiteral(3.0)),
    ])
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
