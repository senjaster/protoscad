from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from manifold_learn.tree.expression import Assignment, NumberLiteral
from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import BuiltinModule


class CubeModule(BuiltinModule):
    def instantiate(self, ctx: EvalContext) -> Manifold:
        size = ctx.args["size"]
        if not isinstance(size, list):
            size = [size, size, size]
        center = bool(ctx.args["center"])
        return Manifold.cube(size, center)

    @property
    def name(self) -> str:
        return "cube"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("size",),
            optional={"center": NumberLiteral(0)},
        )
