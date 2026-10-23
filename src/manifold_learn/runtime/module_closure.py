from __future__ import annotations

from collections.abc import Mapping

from manifold_learn.ast.expression import Assignment, Literal
from manifold_learn.ast.statement import ModuleCallStatement, ModuleDefinitionStatement
from manifold_learn.runtime.children_module import ChildrenModule
from manifold_learn.runtime.environment import Environment
from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import ModuleDefinition


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
        self._defintion_env = env

    def instantiate(self, ctx: EvalContext) -> Geometry | list[Geometry] | None:
        # Bind the call-site parameters as concrete values so the body can
        # resolve them, then instantiate the body in its definition-site
        # environment (lexical) with the call-site environment as the dynamic
        # parent (for $ variables).
        parameters = {name: Assignment(name, Literal(value)) for name, value in ctx.args.items()}
        modules = {"children": ChildrenModule(ctx.children)}
        body_env = Environment(
            variables=parameters,
            modules=modules,
            parent=self._defintion_env,
            dynamic_parent=ctx.env,
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
