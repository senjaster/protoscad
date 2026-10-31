from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection

from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, NumberLiteral


class SquareModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> CrossSection:
        size = ctx.arg_values["size"]
        if not isinstance(size, list):
            size = [size, size]
        return CrossSection.square(size, bool(ctx.arg_values["center"]))

    @property
    def name(self) -> str:
        return "square"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("size",),
            optional={"center": NumberLiteral(0)},
        )
