from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection, JoinType

from protoscad.builtins._fragments import dollar_tessellation, fragments_from_radius
from protoscad.builtins._operations import child_profile
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, Literal, NumberLiteral


class OffsetModule(BuiltinModule):
    """``offset`` — grow or shrink the outlines of 2D children.

    OpenSCAD's parameter reading (offset.cc): an ``r`` rounds the corners
    (arcs sized by the ``$fa``/``$fs`` fragment budgets); a ``delta`` keeps
    them sharp (mitered), and with ``chamfer = true`` cuts them at 45
    degrees instead. ``r`` wins when both are given, and a bare ``offset()``
    is ``r = 1``.
    """

    def instantiate(self, ctx: Invocation) -> CrossSection | None:
        profile = child_profile(ctx, "offset")
        if profile is None:
            return None

        r = ctx.arg_values["r"]
        delta = ctx.arg_values["delta"]
        if r is not None:
            value, join = r, JoinType.Round
        elif delta is not None:
            value, join = delta, JoinType.Square if bool(ctx.arg_values["chamfer"]) else JoinType.Miter
        else:
            value, join = 1, JoinType.Round

        # Round joins replace each corner with an arc of this radius; the
        # fragment rule sizes the arc like it sizes a circle.
        segments = fragments_from_radius(abs(value), *dollar_tessellation(ctx))
        return profile.offset(value, join, circular_segments=segments)

    @property
    def name(self) -> str:
        return "offset"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(optional={"r": Literal(None), "delta": Literal(None), "chamfer": NumberLiteral(0)})
