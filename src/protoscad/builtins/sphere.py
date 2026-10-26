from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, Literal, NumberLiteral


class SphereModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Manifold:
        diameter = ctx.arg_values["d"]
        radius = ctx.arg_values["r"]
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
