from __future__ import annotations

import pytest

from protoscad.builtins._fragments import (
    DEFAULT_FA,
    DEFAULT_FN,
    DEFAULT_FS,
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
