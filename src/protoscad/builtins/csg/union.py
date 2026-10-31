from __future__ import annotations

from collections.abc import Mapping

from protoscad.builtins._operations import Geometry, union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class UnionModule(BuiltinModule):
    """Implicit union of all children.

    Backs bare blocks, the top level, and the user-visible ``union()``.
    """

    def instantiate(self, ctx: Invocation) -> Geometry | None:
        return union_geometries(ctx.evaluate_children())

    @property
    def name(self) -> str:
        return "union"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
