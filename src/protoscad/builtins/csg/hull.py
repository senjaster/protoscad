from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection, Manifold

from protoscad.builtins._operations import Geometry
from protoscad.diagnostics import GeometryError
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class HullModule(BuiltinModule):
    """Creates a convex hull wrapping around all children.

    Works in either dimension — 2D children hull in the plane, 3D children
    in space — but not mixed.
    """

    def instantiate(self, ctx: Invocation) -> Geometry | None:
        geometries = ctx.evaluate_children()
        if not geometries:
            return None
        planar = [geometry for geometry in geometries if isinstance(geometry, CrossSection)]
        if planar:
            if len(planar) != len(geometries):
                raise GeometryError("Cannot combine 2D and 3D children in 'hull'")
            if len(planar) == 1:
                return planar[0].hull()
            return CrossSection.batch_hull(planar)
        if len(geometries) == 1:
            return geometries[0].hull()
        return Manifold.batch_hull(geometries)

    @property
    def name(self) -> str:
        return "hull"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
