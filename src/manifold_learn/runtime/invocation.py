from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any

from manifold_learn.runtime.environment import Environment
from manifold_learn.runtime.module_closure import ModuleClosure
from manifold_learn.tree.expression import Assignment
from manifold_learn.tree.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    VariableBindingStatement,
)

if TYPE_CHECKING:
    from manifold_learn.runtime.module_definition import ModuleDefinition, ParameterBindings


@dataclass
class Invocation:
    """A single module call being evaluated.

    ``node`` is the call statement, ``env`` the scope it appears in;
    everything else about the invocation derives from that pair on demand:
    the resolved ``module``, the ``$``-argument overlay (``call_env``),
    parameter ``bindings``, and the subtree (``children`` statements plus
    the ``child_env`` scope they evaluate in).

    Modules are instantiated with a context and decide themselves whether
    and when to evaluate their children — ``evaluate_children``, or
    per-child ``evaluate`` with a custom environment (a loop binding its
    variable, a module injecting ``$``-variables). That is what lets
    ``if``, ``for`` and ``children()`` exist as ordinary modules instead
    of evaluator special cases.
    """

    node: ModuleCallStatement
    env: Environment

    @classmethod
    def evaluate(cls, node: ModuleCallStatement, env: Environment) -> Any:
        """Evaluate one call statement in the given scope."""
        return cls(node, env).instantiate()

    def instantiate(self) -> Any:
        # Bindings are touched eagerly so argument errors (unknown
        # parameter, arity) surface on every call, even if the module
        # never reads them.
        _ = self.bindings
        return self.module.instantiate(self)

    @cached_property
    def module(self) -> ModuleDefinition:
        # Resolve the module in the caller's scope, not in the scope the
        # call itself introduces for its children.
        module = self.env.lookup_module(self.node.module)
        if module is None:
            raise ValueError(f"Unknown module: {self.node.module!r}")
        return module

    @cached_property
    def call_env(self) -> Environment:
        # `$`-prefixed named arguments are special-variable assignments for
        # this invocation, not parameters. They become an environment layer
        # wrapping the call itself: the module's own arguments and its whole
        # subtree resolve through it, while inner `$` bindings shadow them.
        special_args = {
            name: Assignment(name, expr) for name, expr in self.node.named_args.items() if name.startswith("$")
        }
        if not special_args:
            return self.env
        return self.env.extend_variables(special_args)

    @cached_property
    def bindings(self) -> ParameterBindings:
        # `$`-arguments are not parameters; see ModuleDefinition.bind_parameters
        # for how the remaining arguments bind.
        regular_args = {name: expr for name, expr in self.node.named_args.items() if not name.startswith("$")}
        return self.module.bind_parameters(self.node.positional_args, regular_args)

    @cached_property
    def children(self) -> tuple[ModuleCallStatement, ...]:
        # Only module calls are children; variable bindings and module
        # definitions form the child scope instead (see child_env).
        return tuple(statement for statement in self.node.children if isinstance(statement, ModuleCallStatement))

    @cached_property
    def child_env(self) -> Environment:
        """The scope the call introduces for its children.

        The scope's variable map is built by the environment's
        ``BindingResolver`` strategy (see ``runtime.resolver``): the default
        keeps bindings lazy — forced on first use, memoized, with cycle
        detection on the environment — while the OpenSCAD policy evaluates
        eagerly into constants. Either way the scope is set up even when
        there are no child calls, so unknown-name errors in bindings
        surface. Call arguments and module bodies see the same map
        regardless of source order.
        """
        bindings = [s for s in self.node.children if isinstance(s, VariableBindingStatement)]
        variables = self.call_env.resolver.resolve(self.call_env, bindings)
        return self.child_scope(variables)

    def child_scope(self, variables: dict[str, Assignment]) -> Environment:
        """The child scope carrying the given (already resolved) variables
        plus this scope's module definitions."""
        definitions: list[ModuleDefinitionStatement] = []

        for statement in self.node.children:
            if isinstance(statement, ModuleDefinitionStatement):
                definitions.append(statement)

        scope_env = self.call_env.extend_variables(variables) if variables else self.call_env
        if definitions:
            modules = {
                definition.name: ModuleClosure.from_definition(definition, scope_env) for definition in definitions
            }
            scope_env = scope_env.extend_modules(modules)
        return scope_env

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
        """Evaluate every child, flattening multi-geometry results and
        dropping empty ones.

        The child scope (and with it the scope's variable bindings) is
        built even when there are no child calls: bindings evaluate
        eagerly, like OpenSCAD's compile-time scope setup.
        """
        child_env = self.child_env
        results: list[Any] = []
        for statement in self.children:
            result = self.evaluate(statement, child_env)
            if result is None:
                continue
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results
