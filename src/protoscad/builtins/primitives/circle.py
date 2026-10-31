from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection

from protoscad.builtins._fragments import tessellation_for
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, Literal, NumberLiteral


class CircleModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> CrossSection:
        radius = ctx.arg_values["r"]
        diameter = ctx.arg_values["d"]
        if diameter is not None:
            radius = diameter / 2
        if radius <= 0:
            # OpenSCAD warns and renders nothing for a non-positive radius.
            return CrossSection()
        # OpenSCAD's fragment rule decides the polygon, manifold only draws it.
        return CrossSection.circle(radius, tessellation_for(ctx, radius))

    @property
    def name(self) -> str:
        return "circle"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(optional={"r": NumberLiteral(1), "d": Literal(None)})
