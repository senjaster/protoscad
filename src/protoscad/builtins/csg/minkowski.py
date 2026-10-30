from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class MinkowskiModule(BuiltinModule):
    """Computes the Minkowski sum of all children to round off edges."""

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        geometries = ctx.evaluate_children()
        if not geometries:
            return None
        result = geometries[0]
        for geometry in geometries[1:]:
            result = result.minkowski_sum(geometry)
        return result

    @property
    def name(self) -> str:
        return "minkowski"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
