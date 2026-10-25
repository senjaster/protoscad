from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold, OpType

from manifold_learn.builtins._operations import boolean_geometries
from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import BuiltinModule
from manifold_learn.tree.expression import Assignment


class DifferenceModule(BuiltinModule):
    """Subtracts all subsequent children from the first child."""

    def instantiate(self, ctx: EvalContext) -> Manifold | None:
        return boolean_geometries(ctx.evaluate_children(), OpType.Subtract)

    @property
    def name(self) -> str:
        return "difference"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
