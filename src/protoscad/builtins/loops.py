from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterator, Mapping
from itertools import product
from typing import Any

from manifold3d import Manifold, OpType

from protoscad.builtins._operations import boolean_geometries, union_geometries
from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import ArgBindings, BuiltinModule
from protoscad.tree.expression import Assignment, Expression, Literal
from protoscad.tree.values import RangeValue


class LoopModule(BuiltinModule):
    """Common machinery of ``for`` and ``intersection_for``.

    Every named argument is a loop binding: ``for(i = [0:9], j = [0:9])``.
    Each binding's expression is evaluated once in the calling scope, then
    iterated the OpenSCAD way: a range yields its numbers, a vector its
    elements, anything else a single value. Several bindings nest (the
    leftmost variable is the outermost loop), so the body evaluates once
    per combination.

    The body scope is rebuilt for every combination with the loop variables
    in its base, so body bindings (``for(i = [0:9]) angle = i*36;``) see the
    current iteration's values — and a loop with zero iterations still sets
    a body scope up, so binding errors surface as in any other scope.
    """

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        geometries: list[Manifold] = []
        for bindings in self._iterations(ctx):
            env = ctx.build_child_scope(ctx.call_env.extend_variables(bindings))
            geometries.extend(ctx.evaluate_children(env))
        return self._combine(geometries)

    @abstractmethod
    def _combine(self, geometries: list[Manifold]) -> Manifold | None:
        """Fold one geometry per iteration into the module's result."""
        raise NotImplementedError

    def _iterations(self, ctx: Invocation) -> Iterator[dict[str, Assignment]]:
        """Yield one name → value map per body evaluation, the bindings of
        the loop in source order."""
        bindings = ctx.node.named_args
        if not bindings:
            raise ProtoSCADError(
                f"{self.name}() requires at least one 'variable = values' loop binding",
                code=ErrorCode.INVALID_ARGUMENT,
                span=ctx.node.span,
            )
        steps = [
            (name, self._iteration_values(expression.evaluate(ctx.call_env))) for name, expression in bindings.items()
        ]
        # product iterates the leftmost step slowest — the OpenSCAD nesting order.
        for values in product(*(iteration_values for _, iteration_values in steps)):
            yield {name: Assignment(name, Literal(value)) for (name, _), value in zip(steps, values, strict=True)}

    @staticmethod
    def _iteration_values(value: Any) -> list[Any]:
        """The values one loop variable takes: a range's numbers, a vector's
        elements, anything else as a single value."""
        if isinstance(value, RangeValue):
            return list(value)
        if isinstance(value, list):
            return value
        return [value]

    def bind_args(self, positional_args: list[Expression], named_args: dict[str, Expression]) -> ArgBindings:
        # There are no declared parameters: any named argument is a loop
        # binding (read back via node.named_args), so the unknown-parameter
        # check is replaced by the positional-argument rejection.
        if positional_args:
            raise ProtoSCADError(
                f"{self.name}() takes only 'variable = values' loop bindings, got {len(positional_args)} positional",
                code=ErrorCode.INVALID_ARGUMENT,
                span=positional_args[0].span,
            )
        return ArgBindings(explicit={name: Assignment(name, expr) for name, expr in named_args.items()}, defaults={})

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}


class ForModule(LoopModule):
    """``for(i = [0:9]) { ... }`` — the body unioned over all iterations."""

    def _combine(self, geometries: list[Manifold]) -> Manifold | None:
        return union_geometries(geometries)

    @property
    def name(self) -> str:
        return "for"


class IntersectionForModule(LoopModule):
    """``intersection_for(i = [0:9]) { ... }`` — like ``for``, but the
    iterations are intersected instead of unioned."""

    def _combine(self, geometries: list[Manifold]) -> Manifold | None:
        return boolean_geometries(geometries, OpType.Intersect)

    @property
    def name(self) -> str:
        return "intersection_for"
