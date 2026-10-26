from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, NumberLiteral


class CubeModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Manifold:
        size = ctx.arg_values["size"]
        if not isinstance(size, list):
            size = [size, size, size]
        center = bool(ctx.arg_values["center"])
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
