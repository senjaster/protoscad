from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from manifold_learn.ast.environment import Environment


class Expression:
    """Base class for a node in the expression AST."""

    def evaluate(self, env: "Environment") -> Any:
        raise NotImplementedError


@dataclass
class NumberLiteral(Expression):
    value: float

    def evaluate(self, env: "Environment") -> float:
        return self.value


@dataclass
class Variable(Expression):
    name: str

    def evaluate(self, env: "Environment") -> Any:
        return env.lookup_variable(self.name)


@dataclass
class Assignment:
    """A variable binding: a name plus the expression that defines it.

    Plain data — the scoping rules (self-reference exclusion, parent lookup)
    live in ``Environment``.
    """

    name: str
    value: Expression


@dataclass
class BinaryOp(Expression):
    op: str
    left: Expression
    right: Expression

    def evaluate(self, env: "Environment") -> Any:
        left = self.left.evaluate(env)
        right = self.right.evaluate(env)
        if self.op == "+":
            return left + right
        if self.op == "-":
            return left - right
        if self.op == "*":
            return left * right
        if self.op == "/":
            return left / right
        raise ValueError(f"Unknown binary operator: {self.op!r}")


@dataclass
class Paren(Expression):
    inner: Expression

    def evaluate(self, env: "Environment") -> Any:
        return self.inner.evaluate(env)


@dataclass
class ArrayLiteral(Expression):
    """A list literal, e.g. `[12, var2+2, -3.2]`."""

    elements: list[Expression]

    def evaluate(self, env: "Environment") -> list[Any]:
        return [element.evaluate(env) for element in self.elements]


@dataclass
class Raw(Expression):
    """Placeholder for expression forms not yet modeled (string)."""

    text: str

    def evaluate(self, env: "Environment") -> Any:
        return self.text


@dataclass
class Undefined(Expression):
    """The value of a module parameter that has no default and was not bound.

    Evaluating it is a runtime error: a required parameter was never supplied.
    """

    def evaluate(self, env: "Environment") -> Any:
        raise ValueError("Undefined parameter value")
