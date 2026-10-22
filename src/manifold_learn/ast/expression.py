from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from manifold_learn.ast.tree_node import TreeNode


class Expression:
    """Base class for a node in the expression AST."""

    def evaluate(self, node: "TreeNode") -> Any:
        raise NotImplementedError


@dataclass
class NumberLiteral(Expression):
    value: float

    def evaluate(self, node: "TreeNode") -> float:
        return self.value


@dataclass
class Variable(Expression):
    name: str

    def evaluate(self, node: "TreeNode") -> Any:
        return node.eval_variable(self.name)


@dataclass
class Assignment(Expression):
    """A variable assignment, e.g. `width = 10;`.

    Evaluates the assigned value against a node that excludes this variable,
    so a definition cannot reference itself (OpenSCAD declarative semantics).
    """

    name: str
    value: Expression

    def evaluate(self, node: "TreeNode") -> Any:
        return self.value.evaluate(node.excluding_var(self.name))


@dataclass
class BinaryOp(Expression):
    op: str
    left: Expression
    right: Expression

    def evaluate(self, node: "TreeNode") -> Any:
        left = self.left.evaluate(node)
        right = self.right.evaluate(node)
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

    def evaluate(self, node: "TreeNode") -> Any:
        return self.inner.evaluate(node)


@dataclass
class ArrayLiteral(Expression):
    """A list literal, e.g. `[12, var2+2, -3.2]`."""

    elements: list[Expression]

    def evaluate(self, node: "TreeNode") -> list[Any]:
        return [element.evaluate(node) for element in self.elements]


@dataclass
class Raw(Expression):
    """Placeholder for expression forms not yet modeled (string)."""

    text: str

    def evaluate(self, node: "TreeNode") -> Any:
        return self.text


@dataclass
class Undefined(Expression):
    """The value of a module parameter that has no default and was not bound.

    Evaluating it is a runtime error: a required parameter was never supplied.
    """

    def evaluate(self, node: "TreeNode") -> Any:
        raise ValueError("Undefined parameter value")