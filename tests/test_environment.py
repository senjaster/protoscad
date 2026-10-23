from __future__ import annotations

from manifold_learn.runtime.environment import Environment
from manifold_learn.ast.expression import Assignment, BinaryOp, NumberLiteral, Variable


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


def test_last_definition_wins_in_same_scope():
    env = Environment()
    env.define_variable(Assignment("width", NumberLiteral(10.0)))
    env.define_variable(Assignment("width", NumberLiteral(100.0)))
    assert env.lookup_variable("width") == 100.0


def test_shadowing_references_parent_scope_on_rhs():
    # OpenSCAD declarative semantics: a redefinition in an inner scope may
    # reference the same-named variable from the parent scope on its RHS.
    # The definition must not see itself (no self-reference).
    parent = make_env(x=100.0)
    child = Environment(parent=parent)
    child.define_variable(Assignment("x", BinaryOp("/", Variable("x"), NumberLiteral(2.0))))
    assert child.lookup_variable("x") == 50.0
    assert parent.lookup_variable("x") == 100.0


def test_extend_inherits_variables_and_shadows():
    outer = make_env(x=1.0, y=2.0)
    inner = outer.extend_variables({"y": Assignment("y", NumberLiteral(20.0))})
    assert inner.lookup_variable("x") == 1.0
    assert inner.lookup_variable("y") == 20.0
    assert outer.lookup_variable("y") == 2.0


def test_lookup_module_local():
    marker = object()
    env = Environment(modules={"cube": marker})
    assert env.lookup_module("cube") is marker


def test_lookup_module_falls_back_to_parent():
    marker = object()
    parent = Environment(modules={"cube": marker})
    child = Environment(parent=parent)
    assert child.lookup_module("cube") is marker


def test_lookup_module_missing_returns_none():
    assert Environment().lookup_module("nope") is None


def test_lookup_module_shadows_parent():
    outer_marker = object()
    inner_marker = object()
    outer = Environment(modules={"box": outer_marker})
    inner = Environment(modules={"box": inner_marker}, parent=outer)
    assert inner.lookup_module("box") is inner_marker


# --- $ special variables: dynamically scoped through module boundaries ---


def test_dollar_variable_resolves_lexically_within_a_scope_tree():
    # Assignments reachable through plain lexical nesting are visible
    # without any module boundary involved.
    outer = make_env()
    outer.define_variable(Assignment("$fn", NumberLiteral(50.0)))
    inner = outer.extend_variables()
    assert inner.lookup_variable("$fn") == 50.0


def test_dollar_variable_crosses_module_boundary_via_dynamic_link():
    # $fn is set at the call site; the module body must see it even though
    # its lexical chain leads elsewhere.
    definition_scope = make_env()
    call_scope = make_env()
    call_scope.define_variable(Assignment("$fn", NumberLiteral(50.0)))
    body = Environment.for_module_body({}, definition_scope, call_scope)
    reader = body.extend_variables()
    assert reader.lookup_variable("$fn") == 50.0


def test_dollar_variable_shadows_dynamic_value_inside_body():
    # A $ variable rebound inside the body wins over the call-site value.
    definition_scope = make_env()
    call_scope = make_env()
    call_scope.define_variable(Assignment("$fn", NumberLiteral(50.0)))
    body = Environment.for_module_body({}, definition_scope, call_scope)
    body.define_variable(Assignment("$fn", NumberLiteral(12.0)))
    assert body.lookup_variable("$fn") == 12.0


def test_plain_variable_does_not_cross_module_boundary():
    # Ordinary variables stay lexical: a call-site binding is invisible in
    # the module body.
    definition_scope = make_env()
    call_scope = make_env(x=7.0)
    body = Environment.for_module_body({}, definition_scope, call_scope)
    assert body.lookup_variable("x") is None
    # A definition-site binding IS visible
    definition_scope.define_variable(Assignment("y", NumberLiteral(3.0)))
    assert body.lookup_variable("y") == 3.0


def test_dollar_variable_missing_returns_none():
    body = Environment.for_module_body({}, make_env(), make_env())
    assert body.lookup_variable("$fn") is None
