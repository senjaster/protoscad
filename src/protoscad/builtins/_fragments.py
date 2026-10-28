"""OpenSCAD's fragment-count rule for curved primitives.

Why compute the count here instead of using manifold3d's global tessellation
settings (``set_circular_segments`` / ``set_min_circular_angle`` /
``set_min_circular_edge_length``)? The mapping looks exact but is not:

- Manifold rounds the constrained count up to the nearest multiple of four
  (OpenSCAD: arbitrary integers — $fn=30 must stay 30, not 32).
- Manifold's floor is 4; OpenSCAD floors tiny circles at 5 and forces 5 for
  radii below 1e-3, rules Manifold lacks (r=1 with OpenSCAD's defaults must
  be a pentagon, not a square).
- ``set_circular_segments(n)`` for n < 3 silently does nothing instead of
  OpenSCAD's clamp to 3.
- The settings are process-global with no getters, so per-primitive
  save/restore is impossible; every built-in instantiation would leak
  ``$fn``/``$fa``/``$fs`` into the whole process (and race under threads).

So the port below is the OpenSCAD rule, and the builtins always pass an
explicit count, which Manifold constructors honor verbatim and global state
cannot touch.

One rounding survives regardless: the sphere refines an octahedron, so its
count rounds up to the nearest multiple of four no matter where it came from
(``$fn`` 5-8 all render as the same 8-segment mesh). OpenSCAD's $fn there is
best read as "at least this fine". The cylinder honors every count >= 3
exactly.
"""

from __future__ import annotations

import math

from protoscad.runtime.invocation import Invocation

# Radii below this are "no circle at all" for OpenSCAD's purposes; it
# clamps such fragments to 5 rather than dividing by a near-zero radius.
GRID_COARSE = 1e-3

# OpenSCAD's special-variable defaults, used when the caller's scope
# defines none of them: a full circle per 12 degrees, fragments at least
# 2 mm of arc, $fn off.
DEFAULT_FN = 0.0
DEFAULT_FA = 12.0
DEFAULT_FS = 2.0


def fragments_from_radius(radius: float, fn: float, fs: float, fa: float) -> int:
    """The number of fragments OpenSCAD draws for a circle of ``radius``.

    Port of OpenSCAD's ``get_fragments_from_r``: an explicit ``$fn`` wins
    (clamped to at least 3); otherwise the coarser of the ``$fa`` angle
    budget (360/$fa fragments) and the ``$fs`` arc-length budget
    (2*pi*r/$fs fragments) applies, but never fewer than 5 fragments.
    Non-positive ``$fa``/``$fs`` make their budget vacuous the same way
    OpenSCAD's C++ double math does — the limit goes negative or infinite
    and the 5-fragment floor clamps it.

    The one divergence: OpenSCAD computes ``ceil`` of an infinity when both
    budgets are vacuous (undefined behavior in C++, practically garbage);
    we return the 5-fragment floor instead.
    """
    if radius < GRID_COARSE:
        return 5
    if fn > 0:
        return max(3, int(fn))
    fa_limit = 360.0 / fa if fa != 0 else math.inf
    fs_limit = radius * 2.0 * math.pi / fs if fs != 0 else math.inf
    limit = min(fa_limit, fs_limit)
    if limit == math.inf:
        return 5
    return max(5, math.ceil(limit))


def tessellation_for(ctx: Invocation, radius: float) -> int:
    """Resolve the fragment count for a curved primitive of ``radius``
    from the ``$fn``/``$fa``/``$fs`` visible at the call.

    The call environment is the right lookup point for the same reason it
    is for the primitive's own arguments: ``$``-arguments on the call
    itself (``sphere(r=1, $fn=32)``) and dynamically-scoped ``$``-variables
    from enclosing module calls both resolve there.
    """
    return fragments_from_radius(
        radius,
        fn=_or_default(ctx, "$fn", DEFAULT_FN),
        fs=_or_default(ctx, "$fs", DEFAULT_FS),
        fa=_or_default(ctx, "$fa", DEFAULT_FA),
    )


def _or_default(ctx: Invocation, name: str, default: float) -> float:
    value = ctx.call_env.lookup_variable(name)
    return default if value is None else value
