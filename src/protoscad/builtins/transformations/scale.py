from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection

from protoscad.builtins._operations import Geometry, union_geometries, xy_pair
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class ScaleModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Geometry | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        v = ctx.arg_values["v"]
        if isinstance(child, CrossSection):
            return child.scale(xy_pair(v))
        return child.scale(v)

    @property
    def name(self) -> str:
        return "scale"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("v",))
