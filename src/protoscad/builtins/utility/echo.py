from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from protoscad.builtins._operations import Geometry, union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import ArgBindings, BuiltinModule
from protoscad.tree.expression import Assignment
from protoscad.tree.values import format_echo

if TYPE_CHECKING:
    from protoscad.tree.expression import Expression


def echo_arguments(ctx: Invocation) -> list[tuple[str | None, Any]]:
    """The echo call's arguments, evaluated in the calling scope, as
    ``(name, value)`` pairs — ``None`` names for the positional ones.

    Read off the raw call node: ``echo`` takes any arguments (named ones are
    output bindings, not parameters), so ordinary parameter binding does not
    apply.
    """
    arguments: list[tuple[str | None, Any]] = [(None, expr.evaluate(ctx.call_env)) for expr in ctx.node.positional_args]
    arguments += [(name, expr.evaluate(ctx.call_env)) for name, expr in ctx.node.named_args.items()]
    return arguments


class EchoModule(BuiltinModule):
    """``echo(...)`` prints its arguments on the console in ``ECHO: `` form.

    Debugging aid: the call itself produces no geometry, while children (the
    brace-less or blocked scope after the call) pass through as an implicit
    union — so an ``echo`` can wrap any module call.
    """

    def instantiate(self, ctx: Invocation) -> Geometry | None:
        print("ECHO: " + format_echo(echo_arguments(ctx)))
        return union_geometries(ctx.evaluate_children())

    def bind_args(self, positional_args: list[Expression], named_args: dict[str, Expression]) -> ArgBindings:
        # Any argument is accepted — that is the point of echo. The empty
        # binding also keeps `arg_values` empty; the arguments are read from
        # the call node instead.
        return ArgBindings(explicit={}, defaults={})

    @property
    def name(self) -> str:
        return "echo"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}
