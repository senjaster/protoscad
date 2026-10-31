from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection

from protoscad.builtins._operations import Geometry, union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


def _z_angle(v: float | list[float]) -> float:
    """The in-plane part of a rotate argument: a scalar rotates about z,
    a vector about x, y and z in turn — and only its z entry keeps 2D
    geometry in the plane."""
    if isinstance(v, list):
        return v[2] if len(v) >= 3 else 0.0
    return v


class RotateModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Geometry | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        v = ctx.arg_values["v"]
        if isinstance(child, CrossSection):
            return child.rotate(_z_angle(v))
        return child.rotate(v)

    @property
    def name(self) -> str:
        return "rotate"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("v",))
