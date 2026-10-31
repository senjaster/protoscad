from __future__ import annotations

from collections.abc import Mapping

from manifold3d import OpType

from protoscad.builtins._operations import Geometry, boolean_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class IntersectionModule(BuiltinModule):
    """Keeps only the volume shared by all children."""

    def instantiate(self, ctx: Invocation) -> Geometry | None:
        return boolean_geometries(ctx.evaluate_children(), OpType.Intersect)

    @property
    def name(self) -> str:
        return "intersection"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
