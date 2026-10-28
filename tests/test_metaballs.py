"""Geometry-level tests for the ``metaballs`` module.

These run the real pipeline (parse -> evaluate -> manifold) and assert on the
resulting solid's volume, bounding box and connected components. Volumes are
checked loosely: the marching-tetrahedra surface is an approximation, its
error shrinking with the ``resolution`` grid cell.
"""

from __future__ import annotations

import pytest

from protoscad.builtins import BUILTIN_MODULES
from protoscad.diagnostics import ProtoSCADError
from protoscad.parser import parse_scad
from protoscad.runtime.evaluator import evaluate


def render(source: str):
    return evaluate(parse_scad(source), (module() for module in BUILTIN_MODULES))


def test_single_ball_volume_and_bounds():
    ball = render("metaballs([[0, 0, 0, 5]], resolution = 0.5);")
    assert ball is not None
    # An exact sphere is 4/3*pi*5^3 ~ 523.6; the field is exact for one ball,
    # so the deviation is purely the marching grid.
    assert 480 < ball.volume() < 570
    assert ball.genus() == 0
    assert all(-6.5 <= value <= 6.5 for value in ball.bounding_box())
    # The surface must be reached: the bbox extends to the ball's extent.
    assert all(value <= -4.5 for value in ball.bounding_box()[:3])
    assert all(value >= 4.5 for value in ball.bounding_box()[3:])


def test_blended_balls_merge_into_one_solid():
    # Two r=3 balls 3 mm apart merge when blend=3 (kernel width > gap).
    merged = render("metaballs([[-4.5, 0, 0, 3], [4.5, 0, 0, 3]], blend = 3, resolution = 0.8);")
    assert merged is not None
    assert len(merged.decompose()) == 1


def test_distant_balls_stay_separate():
    # 26 mm of free space cannot bridge with blend=0.5.
    separate = render("metaballs([[0, 0, 0, 2], [30, 0, 0, 2]], blend = 0.5, resolution = 1.0);")
    assert separate is not None
    assert len(separate.decompose()) == 2


def test_capsule_entry():
    capsule = render("metaballs([[0, 0, 0, 10, 0, 0, 2]], resolution = 0.6);")
    assert capsule is not None
    xmin, ymin, zmin, xmax, ymax, zmax = capsule.bounding_box()
    # The surface runs from x=-2 to x=12 with radius 2; the grid bounds add
    # padding, the reported bbox must stay near the true surface.
    assert xmin > -3.2 and xmax < 13.2
    assert ymin > -3.2 and ymax < 3.2
    assert zmin > -3.2 and zmax < 3.2  # Cylinder part pi*4*10 plus two hemispheres 4/3*pi*8.
    assert 130 < capsule.volume() < 190


def test_positional_blend_and_resolution():
    solid = render("metaballs([[0, 0, 0, 5]], 2, 0.5);")
    assert solid is not None
    assert 480 < solid.volume() < 570


def test_resolution_defaults_to_fs():
    solid = render("metaballs([[0, 0, 0, 5]], $fs = 0.5);")
    assert solid is not None
    assert 480 < solid.volume() < 570


@pytest.mark.parametrize(
    "source",
    [
        "metaballs([]);",
        "metaballs(5);",
        "metaballs([[0, 0, 0]]);",
        'metaballs([[0, 0, 0, "a"]]);',
        "metaballs([[0, 0, 0, 5]], blend = 0);",
        "metaballs([[0, 0, 0, 5]], resolution = -1);",
        "metaballs([[0, 0, 0, -3]]);",
        "metaballs([[0, 0, undef, 3]]);",
    ],
)
def test_invalid_arguments_raise(source: str):
    with pytest.raises(ProtoSCADError):
        render(source)
