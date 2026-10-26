from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from protoscad.runtime.environment import Environment
from protoscad.runtime.resolver import DeclarativeResolver, OpenScadResolver
from protoscad.tree.expression import BinaryOp, Expression, NumberLiteral, Variable
from protoscad.tree.statement import VariableBindingStatement


@dataclass
class Branch(Expression):
    """Test double for the future ternary operator.

    Forces the condition, then only the taken branch — the guard that
    makes letrec cycles productive. When the grammar grows ``?:`` its node
    gets these exact semantics, and guarded recursion starts working in
    parsed source too.
    """

    condition: Expression
    then: Expression
    otherwise: Expression

    def evaluate(self, env: Environment) -> Any:
        if self.condition.evaluate(env):
            return self.then.evaluate(env)
        return self.otherwise.evaluate(env)


def make_scope(parent: Environment, *definitions: tuple[str, Expression]) -> Environment:
    """Resolve source-order (name, expression) bindings with the declarative
    policy and return the scope environment."""
    bindings = [VariableBindingStatement(name=name, value=value) for name, value in definitions]
    variables = DeclarativeResolver().resolve(parent, bindings)
    return parent.extend_variables(variables)


GUARDED_SCOPE = (
    ("flag", NumberLiteral(1)),
    ("x", Branch(Variable("flag"), NumberLiteral(10), Variable("y"))),
    ("y", Branch(Variable("flag"), Variable("x"), NumberLiteral(0))),
)


def test_order_does_not_matter():
    # The same scope written forwards and backwards resolves identically.
    forwards = make_scope(
        Environment(),
        ("x", NumberLiteral(10)),
        ("y", BinaryOp("*", Variable("x"), NumberLiteral(2))),
    )
    backwards = make_scope(
        Environment(),
        ("y", BinaryOp("*", Variable("x"), NumberLiteral(2))),
        ("x", NumberLiteral(10)),
    )
    assert forwards.lookup_variable("y") == backwards.lookup_variable("y") == 20.0


def test_redefinition_replaces_definition():
    # Only the last binding of q exists; the unknown zz is never seen.
    scope = make_scope(Environment(), ("q", Variable("zz")), ("q", NumberLiteral(7)))
    assert scope.lookup_variable("q") == 7.0


def test_local_shadows_parent_whole_scope():
    parent = make_scope(Environment(), ("m", NumberLiteral(5)))
    scope = make_scope(parent, ("y", Variable("m")), ("m", NumberLiteral(1)))
    assert scope.lookup_variable("y") == 1.0
    assert parent.lookup_variable("m") == 5.0


def test_self_reference_reads_parent():
    parent = make_scope(Environment(), ("width", NumberLiteral(100)))
    scope = make_scope(parent, ("width", BinaryOp("/", Variable("width"), NumberLiteral(2))))
    assert scope.lookup_variable("width") == 50.0


def test_unknown_name_rejected_at_setup_even_if_unused():
    with pytest.raises(ValueError, match="Unknown variable 'zz'"):
        make_scope(Environment(), ("q", Variable("zz")))


def test_unguarded_cycle_raises_with_forcing_path():
    scope = make_scope(Environment(), ("x", Variable("y")), ("y", Variable("x")))
    with pytest.raises(ValueError, match="Circular variable dependency: x -> y -> x"):
        scope.lookup_variable("x")


def test_unused_unguarded_cycle_is_tolerated():
    scope = make_scope(
        Environment(),
        ("x", Variable("y")),
        ("y", Variable("x")),
        ("z", NumberLiteral(1)),
    )
    assert scope.lookup_variable("z") == 1.0


def test_guarded_cycle_resolves():
    # flag is truthy: x takes its guarded branch immediately, and y's
    # guarded branch reads the memoized x. Neither path forces the cycle.
    scope = make_scope(Environment(), *GUARDED_SCOPE)
    assert scope.lookup_variable("x") == 10.0
    assert scope.lookup_variable("y") == 10.0


def test_guarded_cycle_resolves_forcing_y_first():
    # The same scope, entered from y: memoization makes the order of
    # forcing irrelevant.
    scope = make_scope(Environment(), *GUARDED_SCOPE)
    assert scope.lookup_variable("y") == 10.0
    assert scope.lookup_variable("x") == 10.0


def test_guard_on_taken_branch_still_cycles():
    # The references sit in the branches the guards take: forcing x
    # descends into y, whose guard descends back into x — an unguarded
    # cycle in practice, and the forcing stack catches it.
    scope = make_scope(
        Environment(),
        ("flag", NumberLiteral(1)),
        ("x", Branch(Variable("flag"), Variable("y"), NumberLiteral(10))),
        ("y", Branch(Variable("flag"), Variable("x"), NumberLiteral(0))),
    )
    with pytest.raises(ValueError, match="x -> y -> x"):
        scope.lookup_variable("x")


def test_deep_chain_resolves_in_any_order():
    scope = make_scope(
        Environment(),
        ("height", BinaryOp("/", BinaryOp("+", Variable("depth"), NumberLiteral(5)), NumberLiteral(2))),
        ("depth", BinaryOp("*", Variable("width"), NumberLiteral(2))),
        ("width", NumberLiteral(10)),
    )
    assert scope.lookup_variable("height") == 12.5
    assert scope.lookup_variable("width") == 10.0


def test_openscad_resolver_rejects_cycle_statically_declarative_only_on_use():
    # The eager OpenSCAD policy rejects cycles at setup; the lazy policy
    # waits until the value is used. (Once a real conditional node exists,
    # its both-branch reference set will make the eager policy reject even
    # guarded cycles — the trade-off the lazy policy avoids.)
    # (Written so both names are first-defined before the final mutually
    # recursive bindings — otherwise the OpenSCAD position rule fires
    # first, with its own message.)
    bindings = [
        VariableBindingStatement(name="x", value=NumberLiteral(0)),
        VariableBindingStatement(name="y", value=BinaryOp("+", Variable("x"), NumberLiteral(1))),
        VariableBindingStatement(name="x", value=BinaryOp("+", Variable("y"), NumberLiteral(1))),
    ]
    with pytest.raises(ValueError, match="Circular variable dependency"):
        OpenScadResolver().resolve(Environment(), bindings)
    # The declarative policy builds the scope without complaint...
    scope = make_scope(Environment(), ("x", Variable("y")), ("y", Variable("x")))
    # ...and only raises when the cycle is actually forced.
    with pytest.raises(ValueError, match="Circular variable dependency"):
        scope.lookup_variable("x")
