from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from manifold_learn.ast import ModuleCallStatement
    from manifold_learn.ast.environment import Environment


@dataclass
class ChildInvocation:
    """A child module call held unevaluated, together with the environment
    it must run in.

    ``node`` is a single module call (a child passed to ``children()`` or
    ``evaluate_children()``). Modules decide whether and when to evaluate
    their children (``EvalContext.evaluate_children``). That is what lets
    ``if``, ``for`` and ``children()`` exist as ordinary modules instead of
    evaluator special cases.
    """

    node: ModuleCallStatement
    env: Environment


@dataclass
class EvalContext:
    """Everything a module may use when instantiated."""

    args: Mapping[str, Any]
    children: Sequence[ChildInvocation]
    env: Environment
    evaluate: Callable[[ModuleCallStatement, Environment], Any]

    def evaluate_children(self) -> list[Any]:
        """Evaluate every child invocation, flattening multi-geometry
        results and dropping empty ones."""
        results: list[Any] = []
        for invocation in self.children:
            result = self.evaluate(invocation.node, invocation.env)
            if result is None:
                continue
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results
