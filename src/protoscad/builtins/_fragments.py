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

The same treatment applies to ``linear_extrude``'s default slice count: the
rules at the bottom of this file port OpenSCAD's calc.cc directly rather
than approximating them with a fragment count.
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
    fn, fs, fa = dollar_tessellation(ctx)
    return fragments_from_radius(radius, fn=fn, fs=fs, fa=fa)


def dollar_tessellation(ctx: Invocation) -> tuple[float, float, float]:
    """The ``($fn, $fs, $fa)`` triple visible at the call, defaults filled
    in — the raw budgets, for consumers that slice or fragment by their own
    rule (``extrusion_slices`` below) rather than by radius."""
    return (
        _or_default(ctx, "$fn", DEFAULT_FN),
        _or_default(ctx, "$fs", DEFAULT_FS),
        _or_default(ctx, "$fa", DEFAULT_FA),
    )


def _or_default(ctx: Invocation, name: str, default: float) -> float:
    value = ctx.call_env.lookup_variable(name)
    return default if value is None else value


# =========================================================================
# linear_extrude slice counts

# OpenSCAD's fine-grid threshold (grid.h, 2^-20): below it a profile counts
# as "no shape at all" and only the twist floor constrains the slice count.
GRID_FINE = 0.00000095367431640625


def extrusion_slices(
    radius_sqr: float,
    delta_sqr: float,
    height: float,
    twist: float,
    scale_x: float,
    scale_y: float,
    fn: float,
    fs: float,
    fa: float,
) -> int:
    """How many slices ``linear_extrude`` divides its height into when the
    caller did not pass ``slices`` — a port of OpenSCAD's rule (calc.cc,
    the branches LinearExtrudeNode picks between):

    - twist: enough slices that a corner vertex's path — a helix, or an
      Archimedes spiral when uniform scaling shrinks it toward the apex —
      stays within the ``$fa``/``$fs`` budgets;
    - non-uniform scale without twist: the same budgets over the longest
      vertex diagonal;
    - anything else: a single slice, bottom straight to top.

    ``radius_sqr`` is the largest squared vertex distance from the z axis
    before scaling, ``delta_sqr`` the largest squared vertex displacement
    the top scale causes. Like ``fragments_from_radius``, non-positive
    ``$fa``/``$fs`` make their budget vacuous instead of reproducing
    OpenSCAD's C++ undefined behavior on the division.
    """
    twist = abs(twist)
    if twist != 0:
        if scale_x == scale_y and scale_x != 1.0:
            return _conical_helix_slices(radius_sqr, height, twist, scale_x, fn, fs, fa)
        return _helix_slices(radius_sqr, height, twist, fn, fs, fa)
    if scale_x != scale_y:
        return _diagonal_slices(delta_sqr, height, fn, fs)
    return 1


def _helix_arc_length(radius_sqr: float, height: float, twist: float) -> float:
    # A helix of total angle T and pitch-derived rise c = height/T has arc
    # length T * sqrt(r^2 + c^2).
    t = math.radians(twist)
    c = height / t
    return t * math.sqrt(radius_sqr + c * c)


def _archimedes_length(a: float, theta: float) -> float:
    # Arc length of the spiral r = a*theta from 0 to theta.
    return 0.5 * a * (theta * math.sqrt(1 + theta * theta) + math.asinh(theta))


def _twist_floor(twist: float) -> int:
    # At worst 180 degrees of twist per slice folds flat; keep at least
    # three slices per full turn.
    return max(math.ceil(twist / 120.0), 1)


def _helix_slices(radius_sqr: float, height: float, twist: float, fn: float, fs: float, fa: float) -> int:
    min_slices = _twist_floor(twist)
    if math.sqrt(radius_sqr) < GRID_FINE:
        return min_slices
    if fn > 0:
        return max(math.ceil(twist / 360.0 * fn), min_slices)
    fa_slices = math.ceil(twist / fa) if fa > 0 else math.inf
    fs_slices = math.ceil(_helix_arc_length(radius_sqr, height, twist) / fs) if fs > 0 else math.inf
    return _budgeted_slices(fa_slices, fs_slices, min_slices)


def _conical_helix_slices(
    radius_sqr: float, height: float, twist: float, scale: float, fn: float, fs: float, fa: float
) -> int:
    min_slices = _twist_floor(twist)
    radius = math.sqrt(radius_sqr)
    if radius < GRID_FINE:
        return min_slices
    if fn > 0:
        return max(math.ceil(twist * fn / 360.0), min_slices)
    # The vertex follows a section of the spiral the scale would trace all
    # the way to the apex; find the angular window this twist+scale covers.
    # (Uniform scale is never 1 here — that case takes the plain helix.)
    radians_ = math.radians(twist)
    angle_end = radians_ * scale / (scale - 1) if scale > 1 else radians_ / (1 - scale)
    angle_start = angle_end - radians_
    a = radius / angle_end
    spiral_length = _archimedes_length(a, angle_end) - _archimedes_length(a, angle_start)
    # The flat spiral plus the rise, as a right triangle's legs.
    total_length = math.hypot(spiral_length, height)
    fa_slices = math.ceil(twist / fa) if fa > 0 else math.inf
    fs_slices = math.ceil(total_length / fs) if fs > 0 else math.inf
    return _budgeted_slices(fa_slices, fs_slices, min_slices)


def _budgeted_slices(fa_slices: float, fs_slices: float, min_slices: int) -> int:
    # Both budgets vacuous ($fa and $fs off): the floor, instead of
    # OpenSCAD's cast-of-infinity undefined behavior.
    slices = min(fa_slices, fs_slices)
    if math.isinf(slices):
        return min_slices
    return max(int(slices), min_slices)


def _diagonal_slices(delta_sqr: float, height: float, fn: float, fs: float) -> int:
    if math.sqrt(delta_sqr) < GRID_FINE:
        return 1
    if fn > 0:
        return max(int(fn), 1)
    fs_slices = math.ceil(math.sqrt(delta_sqr + height * height) / fs) if fs > 0 else math.inf
    return 1 if math.isinf(fs_slices) else max(int(fs_slices), 1)
