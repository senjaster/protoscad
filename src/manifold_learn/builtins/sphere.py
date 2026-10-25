from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import BuiltinModule
from manifold_learn.tree.expression import Assignment, Literal, NumberLiteral


class SphereModule(BuiltinModule):
    def instantiate(self, ctx: EvalContext) -> Manifold:
        diameter = ctx.args["d"]
        radius = ctx.args["r"]
        if diameter is not None:
            radius = diameter / 2
        return Manifold.sphere(radius)

    @property
    def name(self) -> str:
        return "sphere"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            optional={"r": NumberLiteral(1), "d": Literal(None)},
        )
