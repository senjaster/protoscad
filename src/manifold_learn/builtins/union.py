from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from manifold_learn.builtins._operations import union_geometries
from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import BuiltinModule
from manifold_learn.tree.expression import Assignment


class UnionModule(BuiltinModule):
    """Implicit union of all children.

    Backs bare blocks, the top level, and the user-visible ``union()``.
    """

    def instantiate(self, ctx: EvalContext) -> Manifold | None:
        return union_geometries(ctx.evaluate_children())

    @property
    def name(self) -> str:
        return "union"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
