from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from manifold_learn.builtins._operations import union_geometries
from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import BuiltinModule
from manifold_learn.tree.expression import Assignment


class TranslateModule(BuiltinModule):
    def instantiate(self, ctx: EvalContext) -> Manifold | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        return child.translate(ctx.args["v"])

    @property
    def name(self) -> str:
        return "translate"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("v",))
