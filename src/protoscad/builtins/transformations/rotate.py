from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.builtins._operations import union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class RotateModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Manifold | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        return child.rotate(ctx.arg_values["v"])

    @property
    def name(self) -> str:
        return "rotate"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("v",))
