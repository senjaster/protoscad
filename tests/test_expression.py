from __future__ import annotations

import pytest

from manifold_learn.ast.expression import (
    ArrayLiteral,
    BinaryOp,
    Expression,
    NumberLiteral,
    Paren,
    Raw,
    Variable, Assignment,
)
from manifold_learn.ast.tree_node import TreeNode


def make_node(**kwargs) -> TreeNode:
    """Build a TreeNode with only the fields the expression tests need."""
    return TreeNode(
        module="root",
        positional_args=[],
        named_args={},
        **kwargs,
    )


def test_expression_base_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        Expression().evaluate(make_node())


def test_number_literal_returns_value():
    assert NumberLiteral(3.5).evaluate(make_node()) == 3.5
    assert NumberLiteral(-2.0).evaluate(make_node()) == -2.0


def test_variable_resolves_through_node():
    node = make_node()
    node.assign_variable(Assignment("x", NumberLiteral(42.0)))
    assert Variable("x").evaluate(node) == 42.0


def test_variable_missing_returns_none():
    assert Variable("nope").evaluate(make_node()) is None


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
    assert expr.evaluate(make_node()) == expected


def test_binary_op_nested():
    # (10 + 20) / 3
    expr = BinaryOp(
        "/",
        BinaryOp("+", NumberLiteral(10.0), NumberLiteral(20.0)),
        NumberLiteral(3.0),
    )
    assert expr.evaluate(make_node()) == 10.0


def test_binary_op_unknown_operator_raises():
    expr = BinaryOp("^", NumberLiteral(2.0), NumberLiteral(3.0))
    with pytest.raises(ValueError):
        expr.evaluate(make_node())


def test_paren_delegates_to_inner():
    inner = BinaryOp("+", NumberLiteral(1.0), NumberLiteral(2.0))
    assert Paren(inner).evaluate(make_node()) == 3.0


def test_raw_returns_text():
    assert Raw("[1, 2, 3]").evaluate(make_node()) == "[1, 2, 3]"


def test_array_literal_evaluates_elements():
    expr = ArrayLiteral([
        NumberLiteral(1.0),
        BinaryOp("+", NumberLiteral(2.0), NumberLiteral(3.0)),
    ])
    assert expr.evaluate(make_node()) == [1.0, 5.0]


def test_array_literal_empty():
    assert ArrayLiteral([]).evaluate(make_node()) == []