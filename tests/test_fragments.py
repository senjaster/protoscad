from __future__ import annotations

import pytest

from protoscad.builtins._fragments import (
    DEFAULT_FA,
    DEFAULT_FN,
    DEFAULT_FS,
    extrusion_slices,
    fragments_from_radius,
)


@pytest.mark.parametrize(
    ("radius", "fn", "fs", "fa", "expected"),
    [
        # Radii too small to be a circle get the floor, not a huge count.
        (0.0005, 0, 2, 12, 5),
        # An explicit $fn wins and truncates to an int.
        (1, 36, 2, 12, 36),
        (1, 36.7, 2, 12, 36),
        # $fn below 3 clamps up to a triangle, matching OpenSCAD.
        (1, 2, 2, 12, 3),
        (1, 0.5, 2, 12, 3),
        # A non-positive $fn is off; the $fa/$fs budgets decide.
        (1, -5, 2, 12, 5),
        (10, 0, 2, 12, 30),  # 360/$fa = 30 beats 2*pi*10/$fs ~ 31.4
        (1, 0, 2, 12, 5),  # 2*pi*1/2 ~ 3.1 -> the 5-fragment floor
        # The budgets take their minimum: $fa=12 caps a fine $fs at 30,
        # and only relaxing $fa lets the arc budget deliver 63.
        (1, 0, 0.1, 12, 30),
        (1, 0, 0.1, 1, 63),
        (10, 0, 1000, 12, 5),  # vacuous $fs -> floor
        # A vacuous $fa drops out of the minimum; the $fs budget decides.
        (10, 0, 2, 0, 32),
        # Non-positive budgets go negative like C++ doubles and clamp to 5.
        (1, 0, -1, 12, 5),
        (1, 0, 2, -5, 5),
        # Both budgets vacuous: floor instead of OpenSCAD's ceil-of-inf UB.
        (1, 0, 0, 0, 5),
    ],
)
def test_fragments_from_radius_matches_openscad(radius, fn, fs, fa, expected):
    assert fragments_from_radius(radius, fn, fs, fa) == expected


def test_builtin_defaults_are_openscads():
    assert DEFAULT_FN == 0
    assert DEFAULT_FA == 12
    assert DEFAULT_FS == 2


## =========================================================================
# linear_extrude default slice counts (OpenSCAD calc.cc)


# All cases share one profile: a square whose farthest vertex sits at
# squared distance 50 from the z axis (square(5) in the first quadrant),
# extruded to height 10. Expected values hand-derived from the formulas in
# the OpenSCAD 2021.01 source (calc.cc / GeometryEvaluator.cc).
@pytest.mark.parametrize(
    ("twist", "scale_x", "scale_y", "delta_sqr", "fn", "fs", "fa", "expected"),
    [
        # Twist with no scaling: the $fa budget gives ceil(90/12) = 8, and
        # the $fs budget over the helix arc (length ~14.94) agrees at 8.
        (90, 1, 1, 0, 0, 2, 12, 8),
        # An explicit $fn slices by angle proportion: ceil(90/360 * 12) = 3.
        (90, 1, 1, 0, 12, 2, 12, 3),
        # A tiny $fn still delivers the 1-slice twist floor.
        (90, 1, 1, 0, 0.5, 2, 12, 1),
        # Full turn: the twist floor is 3, $fa gives 30, $fs gives
        # ceil(45.56/2) = 23.
        (360, 1, 1, 0, 0, 2, 12, 23),
        # Both budgets vacuous: the twist floor instead of cast-of-infinity.
        (360, 1, 1, 0, 0, 0, 0, 3),
        # Vacuous $fs leaves the $fa budget to decide alone.
        (90, 1, 1, 0, 0, 0, 12, 8),
        # Uniform scale with twist follows the shrinking (conical) spiral.
        (90, 0.5, 0.5, 0, 0, 2, 12, 7),
        # Non-uniform scale with twist uses the plain helix rule.
        (90, 1, 0.5, 16, 0, 2, 12, 8),
        # Non-uniform scale alone: the longest vertex diagonal (4) against
        # the extrusion height: ceil(sqrt(16 + 100)/2) = 6.
        (0, 1, 0.2, 16, 0, 2, 12, 6),
        (0, 1, 0.2, 16, 20, 2, 12, 20),
        # Vacuous budgets on the diagonal: the 1-slice floor.
        (0, 1, 0.2, 16, 0, 0, 12, 1),
        # Anything else extrudes bottom straight to top.
        (0, 1, 1, 0, 0, 2, 12, 1),
        (0, 0.5, 0.5, 0, 0, 2, 12, 1),
    ],
)
def test_extrusion_slices_matches_openscad(twist, scale_x, scale_y, delta_sqr, fn, fs, fa, expected):
    assert extrusion_slices(50, delta_sqr, 10, twist, scale_x, scale_y, fn, fs, fa) == expected


def test_extrusion_slices_tiny_profile_takes_the_twist_floor():
    # Below the fine grid (2^-20) the radius carries no information, so
    # only the twist floor (at least 3 slices per full turn) applies.
    assert extrusion_slices(1e-14, 0, 10, 90, 1, 1, 0, 2, 12) == 1
    assert extrusion_slices(1e-14, 0, 10, 360, 1, 1, 0, 2, 12) == 3
