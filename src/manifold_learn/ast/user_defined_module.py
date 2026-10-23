from __future__ import annotations

from typing import Generic, Mapping

from manifold_learn.ast.children_module import ChildrenModule
from manifold_learn.ast.environment import Environment
from manifold_learn.ast.expression import Assignment, Literal
from manifold_learn.ast.module_definition import Geometry, ModuleDefinition
from manifold_learn.ast.invocation import ChildInvocation, EvalContext
from manifold_learn.ast.statement import Statement


class UserDefinedModule(ModuleDefinition, Generic[Geometry]):

    def __init__(
        self,
        name: str,
        parameters: Mapping[str, Assignment],
        body: list[Statement],
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
        parameters = {
            name: Assignment(name, Literal(value)) for name, value in ctx.args.items()
        }
        modules = {"children": ChildrenModule(ctx.children)}
        body_env = Environment(
            variables=parameters,
            modules=modules,
            parent=self._defintion_env,
            dynamic_parent=ctx.env,
            is_module_scope=True,
        )
        body_invocation = ChildInvocation(self._body, body_env)
        return ctx.evaluate(body_invocation)

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self._parameters