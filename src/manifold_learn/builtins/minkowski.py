from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from manifold_learn.tree.expression import Assignment
from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import BuiltinModule


class MinkowskiModule(BuiltinModule):
    """Computes the Minkowski sum of all children to round off edges."""

    def instantiate(self, ctx: EvalContext) -> Manifold | None:
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
