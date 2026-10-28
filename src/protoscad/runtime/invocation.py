from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any

from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.runtime.environment import Environment
from protoscad.runtime.module_closure import ModuleClosure
from protoscad.tree.expression import Assignment, Undefined
from protoscad.tree.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    VariableBindingStatement,
)

if TYPE_CHECKING:
    from protoscad.runtime.module_definition import ArgBindings, ModuleDefinition


@dataclass
class Invocation:
    """A single module call being evaluated.

    ``node`` is the call statement, ``env`` the scope it appears in;
    everything else about the invocation derives from that pair on demand:
    the resolved ``module``, the ``$``-argument overlay (``call_env``),
    the ``arg_bindings``, and the subtree (``children`` statements plus
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
        return cls(node, env)._instantiate()

    def _instantiate(self) -> Any:
        # Bindings are touched eagerly so argument errors (unknown
        # parameter, arity) surface on every call, even if the module
        # never reads them.
        _ = self.arg_bindings
        return self.module.instantiate(self)

    @cached_property
    def module(self) -> ModuleDefinition:
        # Resolve the module in the caller's scope, not in the scope the
        # call itself introduces for its children.
        module = self.env.lookup_module(self.node.module)
        if module is None:
            raise ProtoSCADError(
                f"Unknown module: {self.node.module!r}", code=ErrorCode.UNKNOWN_MODULE, span=self.node.span
            )
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
    def arg_bindings(self) -> ArgBindings:
        # `$`-arguments are not parameters; see ModuleDefinition.bind_args
        # for how the remaining arguments bind. A required parameter left
        # unbound is rejected here rather than at evaluation, so the error
        # points at the call (the argument that would have supplied it does
        # not exist, so the argument spans bind_args uses cannot apply).
        regular_args = {name: expr for name, expr in self.node.named_args.items() if not name.startswith("$")}
        bindings = self.module.bind_args(self.node.positional_args, regular_args)
        for name, parameter in self.module.parameters.items():
            if name not in bindings.explicit and isinstance(parameter.value, Undefined):
                raise ProtoSCADError(
                    f"Missing required parameter {name!r} for module {self.module.name!r}",
                    code=ErrorCode.MISSING_REQUIRED_PARAMETER,
                    span=self.node.span,
                )
        return bindings

    @cached_property
    def children(self) -> tuple[ModuleCallStatement, ...]:
        # Only module calls are children; variable bindings and module
        # definitions form the child scope instead (see child_env).
        return tuple(statement for statement in self.node.children if isinstance(statement, ModuleCallStatement))

    @cached_property
    def child_env(self) -> Environment:
        """The scope the call introduces for its children."""
        return self.build_child_scope(self.call_env)

    def build_child_scope(self, base: Environment) -> Environment:
        """Build the call's child scope over ``base`` instead of the call's
        own environment.

        The scope's variable map is built by the environment's
        ``BindingResolver`` strategy (see ``runtime.resolver``): the default
        keeps bindings lazy — forced on first use, memoized, with cycle
        detection on the environment — while the OpenSCAD policy evaluates
        eagerly into constants. Either way the scope is set up even when
        there are no child calls, so unknown-name errors in bindings
        surface. Call arguments and module bodies see the same map
        regardless of source order.

        ``for`` passes an iteration scope (the call environment plus the
        current loop-variable values) as ``base``, so the body's bindings
        and module definitions rebuild per iteration against those values.
        """
        bindings = [s for s in self.node.children if isinstance(s, VariableBindingStatement)]
        variables = base.resolver.resolve(base, bindings)

        definitions: list[ModuleDefinitionStatement] = []

        for statement in self.node.children:
            if isinstance(statement, ModuleDefinitionStatement):
                definitions.append(statement)

        scope_env = base.extend_variables(variables) if variables else base
        if definitions:
            modules = {
                definition.name: ModuleClosure.from_definition(definition, scope_env) for definition in definitions
            }
            scope_env = scope_env.extend_modules(modules)
        return scope_env

    @cached_property
    def arg_values(self) -> dict[str, Any]:
        """All bound parameters evaluated in the calling scope.

        Convenient for builtins, whose defaults are constants and therefore
        scope-independent. Modules with definition-scoped semantics (user
        modules) must resolve ``arg_bindings`` themselves instead.
        """
        merged: dict[str, Any] = {}
        for name, assignment in self.arg_bindings.explicit.items():
            merged[name] = assignment.value.evaluate(self.call_env)
        for name, assignment in self.arg_bindings.defaults.items():
            merged[name] = assignment.value.evaluate(self.call_env)
        return merged

    def evaluate_children(self, env: Environment | None = None) -> list[Any]:
        """Evaluate every child, flattening multi-geometry results and
        dropping empty ones.

        The child scope (and with it the scope's variable bindings) is
        built even when there are no child calls: bindings evaluate
        eagerly, like OpenSCAD's compile-time scope setup. ``env`` overrides
        where the children evaluate — a loop passes the scope it built for
        the current iteration (see ``build_child_scope``).
        """
        child_env = self.child_env if env is None else env
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
