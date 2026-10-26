from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, Literal, NumberLiteral


class CylinderModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Manifold:
        height = ctx.arg_values["h"]
        radius_low = self._resolve_radius(ctx, "r1", "d1", "r", "d")
        radius_high = self._resolve_radius(ctx, "r2", "d2", "r", "d")
        center = bool(ctx.arg_values["center"])
        return Manifold.cylinder(height, radius_low, radius_high, 0, center)

    @staticmethod
    def _resolve_radius(ctx: Invocation, r_name: str, d_name: str, r_common: str, d_common: str) -> float:
        """Resolve a cylinder radius from the radius/diameter parameters,
        preferring the specific ``rN``/``dN`` over the common ``r``/``d``."""
        for name in (r_name, d_name, r_common, d_common):
            value = ctx.arg_values[name]
            if value is None:
                continue
            if name.startswith("d"):
                return value / 2
            return value
        return 1.0

    @property
    def name(self) -> str:
        return "cylinder"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("h",),
            optional={
                "r": Literal(None),
                "r1": Literal(None),
                "r2": Literal(None),
                "d": Literal(None),
                "d1": Literal(None),
                "d2": Literal(None),
                "center": NumberLiteral(0),
            },
        )
