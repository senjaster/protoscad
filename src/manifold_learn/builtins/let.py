from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from manifold_learn.tree.expression import Assignment
from manifold_learn.builtins._operations import union_geometries
from manifold_learn.runtime.invocation import EvalContext
from manifold_learn.runtime.module_definition import BuiltinModule


class LetModule(BuiltinModule):
    """``let`` is a scope: its leading variable bindings plus a body are
    evaluated declaratively and unioned — the same as a ``union`` module."""

    def instantiate(self, ctx: EvalContext) -> Manifold | None:
        return union_geometries(ctx.evaluate_children())

    @property
    def name(self) -> str:
        return "let"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
