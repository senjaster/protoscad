from __future__ import annotations

import dataclasses
import operator
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from protoscad.runtime.environment import Environment


class Expression:
    """Base class for a node in the expression AST."""

    def evaluate(self, env: Environment) -> Any:
        raise NotImplementedError

    def referenced_names(self) -> set[str]:
        """The names read by this expression (its ``Variable`` leaves).

        Implemented once here by walking the dataclass fields: any field
        that is an ``Expression`` (or a list of them) is a child subtree,
        so new node types participate automatically — as do test doubles
        built from ``Expression``. Only leaf semantics need an override
        (see ``Variable``).
        """
        names: set[str] = set()
        for field in dataclasses.fields(self):  # type: ignore[arg-type]
            value = getattr(self, field.name)
            if isinstance(value, Expression):
                names |= value.referenced_names()
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Expression):
                        names |= item.referenced_names()
        return names


@dataclass
class NumberLiteral(Expression):
    value: float

    def evaluate(self, env: Environment) -> float:
        return self.value


@dataclass
class Literal(Expression):
    """A constant value computed at the call site.

    Used to expose a bound module parameter to the module body: the argument
    expression is evaluated in the caller's scope, and the resulting value is
    wrapped here so the body sees a concrete constant rather than re-resolving
    the original (caller-scoped) expression.
    """

    value: Any

    def evaluate(self, env: Environment) -> Any:
        return self.value


@dataclass
class Variable(Expression):
    name: str

    def evaluate(self, env: Environment) -> Any:
        return env.lookup_variable(self.name)

    def referenced_names(self) -> set[str]:
        return {self.name}


@dataclass
class Assignment:
    """A variable binding: a name plus the expression that defines it.

    Plain data — the scoping rules (self-reference exclusion, parent lookup)
    live in ``Environment``.
    """

    name: str
    value: Expression


# Runtime semantics of the binary operators, shared by evaluation and
# constant folding. New operators are added here and in the grammar only.
OPERATORS: dict[str, Callable[[Any, Any], Any]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


@dataclass
class BinaryOp(Expression):
    op: str
    left: Expression
    right: Expression

    def __post_init__(self) -> None:
        # Resolved once: evaluate() runs on every lookup of every node.
        # An unknown operator cannot come from the grammar, so failing at
        # construction is the right place.
        try:
            self._fn = OPERATORS[self.op]
        except KeyError:
            raise ValueError(f"Unknown binary operator: {self.op!r}") from None

    def evaluate(self, env: Environment) -> Any:
        return self._fn(self.left.evaluate(env), self.right.evaluate(env))


@dataclass
class Paren(Expression):
    inner: Expression

    def evaluate(self, env: Environment) -> Any:
        return self.inner.evaluate(env)


@dataclass
class ArrayLiteral(Expression):
    """A list literal, e.g. `[12, var2+2, -3.2]`."""

    elements: list[Expression]

    def evaluate(self, env: Environment) -> list[Any]:
        return [element.evaluate(env) for element in self.elements]


@dataclass
class Raw(Expression):
    """Placeholder for expression forms not yet modeled (string)."""

    text: str

    def evaluate(self, env: Environment) -> Any:
        return self.text


@dataclass
class Undefined(Expression):
    """The value of a module parameter that has no default and was not bound.

    Evaluating it is a runtime error: a required parameter was never supplied.
    """

    def evaluate(self, env: Environment) -> Any:
        raise ValueError("Undefined parameter value")


def _constant(node: Expression) -> tuple[bool, Any]:
    """Whether ``node`` is a constant, and its Python value if so."""
    if isinstance(node, NumberLiteral | Literal):
        return True, node.value
    if isinstance(node, Raw):
        return True, node.text
    return False, None


def fold(node: Expression) -> Expression:
    """Constant-fold an expression subtree, bottom-up.

    Literal-only arithmetic collapses to a single literal, and an array of
    constants to a ``Literal`` list — the shapes real .scad files are full
    of (``[6, 10, 10]``, ``$fn/4 + 2``). Arithmetic on two number literals
    stays a ``NumberLiteral``. Folding is best-effort: an operation that
    would fail at run time (``1/0``, ``[1]+2``) is left unfolded, so the
    error surfaces at evaluation, in context.
    """
    if isinstance(node, BinaryOp):
        left, right = fold(node.left), fold(node.right)
        left_constant, left_value = _constant(left)
        right_constant, right_value = _constant(right)
        if left_constant and right_constant:
            try:
                value = OPERATORS[node.op](left_value, right_value)
            except Exception:
                # Folding must never fail construction on an unfoldable
                # operation.
                return BinaryOp(node.op, left, right)
            if isinstance(left, NumberLiteral) and isinstance(right, NumberLiteral):
                return NumberLiteral(value)
            return Literal(value)
        return BinaryOp(node.op, left, right)
    if isinstance(node, Paren):
        inner = fold(node.inner)
        is_constant, _ = _constant(inner)
        return inner if is_constant else Paren(inner)
    if isinstance(node, ArrayLiteral):
        elements = [fold(element) for element in node.elements]
        constants = [_constant(element) for element in elements]
        if all(is_constant for is_constant, _ in constants):
            return Literal([value for _, value in constants])
        return ArrayLiteral(elements)
    return node
