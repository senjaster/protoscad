from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment
from protoscad.tree.values import truthy


class IfModule(BuiltinModule):
    """``if (condition) {...}`` / ``if (condition) {...} else {...}``.

    The grammar lowers the construct into one ``if`` call with at most two
    children: the true branch, then the false branch (absent without
    ``else``), each a single implicit-union scope. Instantiating evaluates
    the taken branch and nothing else, so the untaken branch builds no
    scope and its bindings never resolve.
    """

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        branch = 0 if truthy(ctx.arg_values["condition"]) else 1
        if branch >= len(ctx.children):
            return None
        return ctx.evaluate(ctx.children[branch], ctx.child_env)

    @property
    def name(self) -> str:
        return "if"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=["condition"])
