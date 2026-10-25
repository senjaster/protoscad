from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from functools import cached_property
from typing import TYPE_CHECKING, Any

from manifold_learn.runtime.module_definition import ParameterBindings

if TYPE_CHECKING:
    from manifold_learn.runtime.environment import Environment
    from manifold_learn.tree import ModuleCallStatement


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
    """Everything a module may use when instantiated.

    Two environments are exposed because a module call sits between two
    scopes:

    - ``call_env`` is the scope the call appears in; explicit argument
      expressions resolve there.
    - ``children_env`` is the scope the module instantiates its subtree in —
      the environment every ``ChildInvocation`` in ``children`` carries
      (plus any ``$``-argument overlay); user module bodies get it as their
      dynamic parent so special variables reach them.
    """

    bindings: ParameterBindings
    call_env: Environment
    children_env: Environment
    evaluate: Callable[[ModuleCallStatement, Environment], Any]
    children: Sequence[ChildInvocation] = field(default_factory=tuple)

    @cached_property
    def args(self) -> dict[str, Any]:
        """All bound parameters evaluated in the calling scope.

        Convenient for builtins, whose defaults are constants and therefore
        scope-independent. Modules with definition-scoped semantics (user
        modules) must resolve ``bindings`` themselves instead.
        """
        merged: dict[str, Any] = {}
        for name, assignment in self.bindings.explicit.items():
            merged[name] = assignment.value.evaluate(self.call_env)
        for name, assignment in self.bindings.defaults.items():
            merged[name] = assignment.value.evaluate(self.call_env)
        return merged

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
