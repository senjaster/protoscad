from __future__ import annotations

from typing import Any

import pytest

from protoscad.runtime.environment import Environment
from protoscad.tree.expression import Assignment, BinaryOp, Expression, NumberLiteral, Variable


def make_env(**variables: float) -> Environment:
    return Environment(variables={name: Assignment(name, NumberLiteral(value)) for name, value in variables.items()})


def test_lookup_local_variable():
    env = make_env(x=5.0)
    assert env.lookup_variable("x") == 5.0


def test_lookup_falls_back_to_parent():
    parent = make_env(x=10.0)
    child = Environment(parent=parent)
    assert child.lookup_variable("x") == 10.0


def test_lookup_missing_returns_none():
    assert Environment().lookup_variable("nope") is None


def test_child_scope_shadows_parent():
    parent = make_env(x=10.0)
    child = Environment(variables={"x": Assignment("x", NumberLiteral(99.0))}, parent=parent)
    assert child.lookup_variable("x") == 99.0
    assert parent.lookup_variable("x") == 10.0


def test_extend_inherits_variables_and_shadows():
    outer = make_env(x=1.0, y=2.0)
    inner = outer.extend_variables({"y": Assignment("y", NumberLiteral(20.0))})
    assert inner.lookup_variable("x") == 1.0
    assert inner.lookup_variable("y") == 20.0
    assert outer.lookup_variable("y") == 2.0


def test_lookup_module_local():
    marker: Any = object()
    env = Environment(modules={"cube": marker})
    assert env.lookup_module("cube") is marker


def test_lookup_module_falls_back_to_parent():
    marker: Any = object()
    parent = Environment(modules={"cube": marker})
    child = Environment(parent=parent)
    assert child.lookup_module("cube") is marker


def test_lookup_module_missing_returns_none():
    assert Environment().lookup_module("nope") is None


def test_lookup_module_shadows_parent():
    outer_marker: Any = object()
    inner_marker: Any = object()
    outer = Environment(modules={"box": outer_marker})
    inner = Environment(modules={"box": inner_marker}, parent=outer)
    assert inner.lookup_module("box") is inner_marker


# --- $ special variables: dynamically scoped through module boundaries ---


def test_dollar_variable_resolves_lexically_within_a_scope_tree():
    # Assignments reachable through plain lexical nesting are visible
    # without any module boundary involved.
    outer = make_env(**{"$fn": 50.0})
    inner = outer.extend_variables()
    assert inner.lookup_variable("$fn") == 50.0


def test_dollar_variable_crosses_module_boundary_via_dynamic_link():
    # $fn is set at the call site; the module body must see it even though
    # its lexical chain leads elsewhere.
    definition_scope = make_env()
    call_scope = make_env(**{"$fn": 50.0})
    body = Environment.for_module_body({}, definition_scope, call_scope)
    reader = body.extend_variables()
    assert reader.lookup_variable("$fn") == 50.0


def test_dollar_variable_shadows_dynamic_value_inside_body():
    # A $ variable rebound inside the body wins over the call-site value.
    definition_scope = make_env()
    call_scope = make_env(**{"$fn": 50.0})
    body = Environment.for_module_body({"$fn": Assignment("$fn", NumberLiteral(12.0))}, definition_scope, call_scope)
    assert body.lookup_variable("$fn") == 12.0


def test_dollar_variable_missing_returns_none():
    body = Environment.for_module_body({}, make_env(), make_env())
    assert body.lookup_variable("$fn") is None


## =========================================================================
#  Memoized binding values


class CountingExpression(Expression):
    """A non-constant node counting how many times it was evaluated."""

    def __init__(self) -> None:
        self.calls = 0

    def evaluate(self, env: Environment) -> float:
        self.calls += 1
        return 42.0


def test_binding_evaluated_once_per_scope():
    counting = CountingExpression()
    env = Environment(variables={"x": Assignment("x", counting)})
    assert env.lookup_variable("x") == 42.0
    assert env.lookup_variable("x") == 42.0
    assert counting.calls == 1


def test_sibling_referenced_twice_evaluated_once():
    # x = y + y: both `y` reads hit the memoized value, so the binding
    # behind `y` runs once.
    counting = CountingExpression()
    env = Environment(
        variables={
            "y": Assignment("y", counting),
            "x": Assignment("x", BinaryOp("+", Variable("y"), Variable("y"))),
        }
    )
    assert env.lookup_variable("x") == 84.0
    assert env.lookup_variable("x") == 84.0
    assert counting.calls == 1


def test_failed_evaluation_is_not_cached():
    class FailingExpression(Expression):
        def evaluate(self, env: Environment) -> float:
            raise RuntimeError("boom")

    env = Environment(variables={"x": Assignment("x", FailingExpression())})
    for _ in range(2):
        with pytest.raises(RuntimeError, match="boom"):
            env.lookup_variable("x")
