from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class HullModule(BuiltinModule):
    """Creates a convex hull wrapping around all children."""

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        geometries = ctx.evaluate_children()
        if not geometries:
            return None
        if len(geometries) == 1:
            return geometries[0].hull()
        return Manifold.batch_hull(geometries)

    @property
    def name(self) -> str:
        return "hull"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
