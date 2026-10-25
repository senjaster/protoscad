from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from manifold_learn.runtime.children_module import ChildrenModule
from manifold_learn.runtime.environment import Environment
from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import ModuleDefinition
from manifold_learn.tree.expression import Assignment, Literal
from manifold_learn.tree.statement import ModuleCallStatement, ModuleDefinitionStatement


class ModuleClosure[Geometry](ModuleDefinition):
    def __init__(
        self,
        name: str,
        parameters: Mapping[str, Assignment],
        body: ModuleCallStatement,
        env: Environment,
    ):
        self._name = name
        self._parameters = parameters
        self._body = body
        self._definition_env = env

    def instantiate(self, ctx: EvalContext) -> Geometry | list[Geometry] | None:
        # Explicit arguments resolve in the caller's scope; defaults resolve
        # where the module was defined — the same lexical scope the body
        # sees — so a default like `module Foo(b = width * 2)` follows the
        # definition-site `width`, not whatever is in scope at the call.
        values: dict[str, Any] = {
            name: assignment.value.evaluate(ctx.call_env) for name, assignment in ctx.bindings.explicit.items()
        }
        for name, assignment in ctx.bindings.defaults.items():
            values[name] = assignment.value.evaluate(self._definition_env)

        # Re-wrap the evaluated values as constants so the body resolves
        # parameters without re-running caller-scoped expressions.
        parameters = {name: Assignment(name, Literal(value)) for name, value in values.items()}
        modules = {"children": ChildrenModule(ctx.children)}
        body_env = Environment(
            variables=parameters,
            modules=modules,
            parent=self._definition_env,
            dynamic_parent=ctx.children_env,
            is_module_scope=True,
        )
        return ctx.evaluate(self._body, body_env)

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self._parameters

    @classmethod
    def from_definition(cls, module: ModuleDefinitionStatement, env: Environment) -> ModuleClosure:
        return cls(module.name, module.parameters, module.body, env)
