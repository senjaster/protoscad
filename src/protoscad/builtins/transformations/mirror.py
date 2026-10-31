from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection

from protoscad.builtins._operations import Geometry, union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class MirrorModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Geometry | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        v = ctx.arg_values["v"]
        if isinstance(child, CrossSection):
            # A plane mirror normal projected on the plane: xy components.
            return child.mirror(v[:2] if isinstance(v, list) else v)
        return child.mirror(v)

    @property
    def name(self) -> str:
        return "mirror"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("v",))
