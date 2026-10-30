from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.builtins._operations import union_geometries
from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, UndefLiteral
from protoscad.tree.values import format_assertion_failure, truthy


class AssertModule(BuiltinModule):
    """``assert(condition, message?)`` — raises unless the condition holds.

    The message (any value, printed the way ``echo`` shows it) is optional.
    A passing assert is a pass-through scope: children evaluate and union,
    so an ``assert`` can guard any module call. The failure points at the
    assert's own span, so the source snippet shows the checked condition.
    """

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        values = ctx.arg_values
        if not truthy(values["condition"]):
            raise ProtoSCADError(
                format_assertion_failure(values["message"]),
                code=ErrorCode.ASSERTION_FAILED,
                span=ctx.node.span,
            )
        return union_geometries(ctx.evaluate_children())

    @property
    def name(self) -> str:
        return "assert"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=["condition"], optional={"message": UndefLiteral()})
