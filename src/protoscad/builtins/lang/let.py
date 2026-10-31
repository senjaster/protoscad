from __future__ import annotations

from collections.abc import Mapping

from protoscad.builtins._operations import Geometry, union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class LetModule(BuiltinModule):
    """``let`` is a scope: its leading variable bindings plus a body are
    evaluated declaratively and unioned — the same as a ``union`` module."""

    def instantiate(self, ctx: Invocation) -> Geometry | None:
        return union_geometries(ctx.evaluate_children())

    @property
    def name(self) -> str:
        return "let"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
