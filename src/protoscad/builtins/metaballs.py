"""Implicit modeling: ``metaballs`` over Manifold's marching tetrahedra.

``Manifold.level_set`` builds a manifold from a signed-distance function, but
takes a *callable* — a thing the language has no syntax for. This module keeps
that machinery internal: the field is synthesized by the interpreter from
plain vector data (``[x, y, z, r]`` balls and ``[x1, y1, z1, x2, y2, z2, r]``
capsules), blended with an exponential smooth-min. The user writes a list of
numbers and receives one solid — the classic organic multi-lobe shape that
CSG cannot express directly.

Two conventions matter here and both are easy to get silently wrong:

- Manifold's ``level_set`` builds the region where the field is POSITIVE
  (verified empirically: a positive-outside distance field yields the
  complement of the shape, despite the docstring's wording). The field below
  is therefore inside-positive — the negation of the usual SDF convention.
- The exponential smooth-min lets a solid bulge up to ``blend * ln(n)``
  beyond the nearest ball's surface (that bulge *is* the metaball attraction),
  so the marching grid's bounds are padded by that bound plus one grid cell.
"""

from __future__ import annotations

import math
from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.builtins._fragments import DEFAULT_FS, _or_default
from protoscad.diagnostics import ErrorCode, ProtoSCADError, SourceSpan
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, Literal, NumberLiteral
from protoscad.tree.values import is_number, type_of

# A ball is [x, y, z, r]; a capsule adds a second endpoint: [x1, y1, z1, x2, y2, z2, r].
_BALL = 4
_CAPSULE = 7


def _entry_distance(entry: tuple[float, ...], x: float, y: float, z: float) -> float:
    """The usual signed distance (negative inside) for one ball or capsule."""
    if len(entry) == _CAPSULE:
        ax, ay, az, bx, by, bz, radius = entry
        pax, pay, paz = x - ax, y - ay, z - az
        bax, bay, baz = bx - ax, by - ay, bz - az
        axis_length_squared = bax * bax + bay * bay + baz * baz
        if axis_length_squared <= 0.0:
            distance_squared = pax * pax + pay * pay + paz * paz
        else:
            h = (pax * bax + pay * bay + paz * baz) / axis_length_squared
            h = min(1.0, max(0.0, h))
            dx, dy, dz = pax - bax * h, pay - bay * h, paz - baz * h
            distance_squared = dx * dx + dy * dy + dz * dz
        return math.sqrt(distance_squared) - radius
    cx, cy, cz, radius = entry
    return math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) - radius


def _parse_balls(value: object, span: SourceSpan | None) -> list[tuple[float, ...]]:
    """Validate the ``balls`` argument: a non-empty vector of numeric
    4-vectors (balls) or 7-vectors (capsules), all finite, radii positive."""
    if not isinstance(value, list) or not value:
        raise ProtoSCADError(
            f"metaballs() expects a non-empty vector of balls, got {type_of(value).value}",
            code=ErrorCode.INVALID_ARGUMENT,
            span=span,
        )
    entries: list[tuple[float, ...]] = []
    for index, entry in enumerate(value):
        kind = f"ball {index}"
        if not isinstance(entry, list) or len(entry) not in (_BALL, _CAPSULE):
            raise ProtoSCADError(
                f"metaballs() {kind} must be [x, y, z, r] or [x1, y1, z1, x2, y2, z2, r], "
                f"got {type_of(entry).value} of length {len(entry) if isinstance(entry, list) else '-'}",
                code=ErrorCode.INVALID_ARGUMENT,
                span=span,
            )
        if not all(is_number(component) for component in entry):
            raise ProtoSCADError(
                f"metaballs() {kind} must be all numbers, "
                f"found {next(type_of(c).value for c in entry if not is_number(c))}",
                code=ErrorCode.INVALID_ARGUMENT,
                span=span,
            )
        numbers = tuple(float(component) for component in entry)
        if not all(math.isfinite(component) for component in numbers):
            raise ProtoSCADError(
                f"metaballs() {kind} must be finite numbers",
                code=ErrorCode.INVALID_ARGUMENT,
                span=span,
            )
        radius = numbers[3]
        if radius <= 0:
            raise ProtoSCADError(
                f"metaballs() {kind} radius must be positive, got {radius}",
                code=ErrorCode.INVALID_ARGUMENT,
                span=span,
            )
        entries.append(numbers)
    return entries


def _positive_number(ctx: Invocation, name: str, value: object) -> float:
    if not is_number(value):
        raise ProtoSCADError(
            f"metaballs() parameter {name!r} must be a positive number, got {type_of(value).value}",
            code=ErrorCode.INVALID_ARGUMENT,
            span=ctx.node.span,
        )
    number = float(value)
    if number <= 0:
        raise ProtoSCADError(
            f"metaballs() parameter {name!r} must be a positive number, got {number}",
            code=ErrorCode.INVALID_ARGUMENT,
            span=ctx.node.span,
        )
    return number


class MetaballsModule(BuiltinModule):
    """``metaballs([[x, y, z, r], ...], blend = 2, resolution)``.

    ``blend`` is the smooth-min kernel width: larger values merge balls from
    further apart and round the junctions more. ``resolution`` is the marching
    grid cell size; by default it follows ``$fs`` (the same "minimum detail
    size" special variable the curved primitives read), so
    ``metaballs(..., $fs = 0.5)`` refines like a fine ``cylinder``.

    The result is a single solid: the smooth union of all entries, genus 0
    while they connect, separate components when they do not.
    """

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        balls = _parse_balls(ctx.arg_values["balls"], ctx.node.span)
        blend = _positive_number(ctx, "blend", ctx.arg_values["blend"])
        resolution = ctx.arg_values["resolution"]
        if resolution is None:
            resolution = _or_default(ctx, "$fs", DEFAULT_FS)
        resolution = _positive_number(ctx, "resolution", resolution)

        bounds = self._bounds(balls, blend, resolution)

        inverse_blend = 1.0 / blend

        def field(x: float, y: float, z: float) -> float:
            # Inside-positive smooth union. Log-sum-exp keeps e^{a/k} from
            # overflowing deep inside large balls: factor out the largest
            # scaled depth, leaving only arguments <= 0.
            scaled = [-_entry_distance(entry, x, y, z) * inverse_blend for entry in balls]
            peak = max(scaled)
            total = sum(math.exp(value - peak) for value in scaled)
            return blend * (peak + math.log(total))

        result = Manifold.level_set(field, bounds, resolution)
        return None if result.is_empty() else result

    @staticmethod
    def _bounds(entries: list[tuple[float, ...]], blend: float, resolution: float) -> tuple[float, ...]:
        """The marching grid extent: every entry's bounding box padded by the
        smooth-min bulge bound (``blend * ln(n)``) plus one grid cell."""
        pad = blend * (math.log(len(entries)) + 1.0) + resolution
        mins = [math.inf, math.inf, math.inf]
        maxs = [-math.inf, -math.inf, -math.inf]
        for entry in entries:
            corners = (entry[0:3], entry[3:6]) if len(entry) == _CAPSULE else (entry[0:3],)
            for corner in corners:
                for axis in range(3):
                    mins[axis] = min(mins[axis], corner[axis] - entry[-1])
                    maxs[axis] = max(maxs[axis], corner[axis] + entry[-1])
        return (
            mins[0] - pad,
            mins[1] - pad,
            mins[2] - pad,
            maxs[0] + pad,
            maxs[1] + pad,
            maxs[2] + pad,
        )

    @property
    def name(self) -> str:
        return "metaballs"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("balls",),
            optional={
                "blend": NumberLiteral(2),
                "resolution": Literal(None),
            },
        )
