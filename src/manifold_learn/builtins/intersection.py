from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold, OpType

from manifold_learn.builtins._operations import boolean_geometries
from manifold_learn.runtime.invocation import Invocation
from manifold_learn.runtime.module_definition import BuiltinModule
from manifold_learn.tree.expression import Assignment


class IntersectionModule(BuiltinModule):
    """Keeps only the volume shared by all children."""

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        return boolean_geometries(ctx.evaluate_children(), OpType.Intersect)

    @property
    def name(self) -> str:
        return "intersection"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
