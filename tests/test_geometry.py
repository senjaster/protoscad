"""End-to-end geometry checks: source text in, Manifold properties out.

These test what the interpreter *renders*, not just which modules it calls:
volumes and bounding boxes of the geometry that real builtins produce.
"""

from __future__ import annotations

import math

import pytest
from manifold3d import Manifold

from protoscad.builtins import BUILTIN_MODULES
from protoscad.parser import parse_scad
from protoscad.runtime.evaluator import evaluate

IDEAL_SPHERE_1 = 4.0 / 3.0 * math.pi
IDEAL_CYLINDER_10_1 = math.pi * 10

# Regular-n-gon prism volumes: n/2 * sin(2*pi/n) * r^2 * height.
PENTAGON_10_1 = 10 * 2.5 * math.sin(2 * math.pi / 5)


def render(source: str) -> Manifold | None:
    return evaluate(parse_scad(source), (factory() for factory in BUILTIN_MODULES))


def polygon_prism(fragments: int, height: float = 10.0, radius: float = 1.0) -> float:
    return height * (fragments / 2) * math.sin(2 * math.pi / fragments) * radius**2


## =========================================================================
# $fn/$fa/$fs drive cylinder tessellation


def test_default_cylinder_is_the_openscad_default_pentagon():
    # $fa=12, $fs=2 defaults: for r=1 the $fs arc budget binds and the
    # 5-fragment floor applies, exactly like OpenSCAD.
    assert render("cylinder(h = 10, r = 1);").volume() == pytest.approx(PENTAGON_10_1)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("cylinder(h = 10, r = 1, $fn = 3);", pytest.approx(polygon_prism(3))),
        ("cylinder(h = 10, r = 1, $fn = 2);", pytest.approx(polygon_prism(3))),  # $fn clamps up to 3
        ("cylinder(h = 10, r = 1, $fn = 6);", pytest.approx(polygon_prism(6))),
        ("cylinder(h = 10, r = 1, $fn = 8);", pytest.approx(polygon_prism(8))),
        ("cylinder(h = 10, r = 1, $fs = 1000);", pytest.approx(polygon_prism(5))),  # vacuous $fs
        ("cylinder(h = 10, r = 1, $fa = 6);", pytest.approx(polygon_prism(5))),  # $fs still binds
        ("cylinder(h = 10, r = 1, $fn = 0);", pytest.approx(polygon_prism(5))),  # explicit off
        ("cylinder(h = 10, r = 1, $fn = 8, $fs = 0.01);", pytest.approx(polygon_prism(8))),  # $fn wins
        # $fa=12 caps the fine $fs budget at 30 fragments (0.7% under ideal).
        ("cylinder(h = 10, r = 1, $fs = 0.1);", pytest.approx(polygon_prism(30))),
        ("cylinder(h = 10, r = 1, $fs = 0.1, $fa = 1);", pytest.approx(IDEAL_CYLINDER_10_1, rel=0.005)),
        ("cylinder(h = 10, r = 1, $fn = 64);", pytest.approx(IDEAL_CYLINDER_10_1, rel=0.005)),
    ],
)
def test_cylinder_fragment_count(source, expected):
    assert render(source).volume() == expected


def test_cone_tessellates_by_the_larger_radius():
    # Square-pyramid volume with $fn=4: the count comes from r1=2, not r2.
    pyramid = 10 * (4 / 2) * math.sin(math.pi / 2) * 2**2 / 3
    assert render("cylinder(h = 10, r1 = 2, r2 = 0, $fn = 4);").volume() == pytest.approx(pyramid)


## =========================================================================
# $fn/$fa/$fs drive sphere tessellation


def test_sphere_fragment_count_converges_on_the_ideal_volume_from_below():
    coarse = render("sphere($fn = 4);").volume()
    medium = render("sphere($fn = 16);").volume()
    fine = render("sphere($fn = 64);").volume()
    assert 0 < coarse < medium < fine < IDEAL_SPHERE_1
    assert fine == pytest.approx(IDEAL_SPHERE_1, rel=0.01)


def test_sphere_bbox_is_exact_regardless_of_fragment_count():
    expected = (-1.0, -1.0, -1.0, 1.0, 1.0, 1.0)
    assert render("sphere(1);").bounding_box() == pytest.approx(expected)
    assert render("sphere(1, $fn = 32);").bounding_box() == pytest.approx(expected)


def test_sphere_d_and_r_agree_under_the_same_fragment_count():
    assert render("sphere(d = 2, $fn = 32);").volume() == pytest.approx(render("sphere(r = 1, $fn = 32);").volume())


def test_sphere_fragment_count_quantizes_to_fours():
    # Manifold builds spheres by refining an octahedron, so the requested
    # count is always rounded UP to the nearest multiple of four (its
    # docstring says so): $fn 5-8 all yield the same 8-segment mesh, and
    # the two-argument constructor's count is not honored verbatim the way
    # cylinder's is.
    coarse = render("sphere($fn = 4);").volume()
    same_mesh = [render(f"sphere($fn = {k});").volume() for k in (5, 6, 7, 8)]
    finer = render("sphere($fn = 9);").volume()
    assert all(v == pytest.approx(same_mesh[0]) for v in same_mesh)
    assert coarse < same_mesh[0] < finer


## =========================================================================
# $-variable scoping reaches the tessellation


def test_dollar_fn_applies_lexically_from_an_assignment():
    source = """
    $fn = 64;
    cylinder(h = 10, r = 1);
    """
    assert render(source).volume() == pytest.approx(IDEAL_CYLINDER_10_1, rel=0.005)


def test_dollar_fn_reaches_a_user_module_body_dynamically():
    source = """
    module pipe() { cylinder(h = 10, r = 1); }
    pipe($fn = 64);
    """
    assert render(source).volume() == pytest.approx(IDEAL_CYLINDER_10_1, rel=0.005)


def test_dollar_fn_stops_at_the_module_call_boundary():
    # The special argument scopes to its call's subtree only: a second,
    # unannotated call renders at the default 5-fragment resolution. The
    # union of the two disjoint cylinders has exactly the two volumes sum.
    source = """
    module pipe() { cylinder(h = 10, r = 1); }
    pipe($fn = 64);
    translate([5, 0, 0]) pipe();
    """
    expected = polygon_prism(64) + PENTAGON_10_1
    assert render(source).volume() == pytest.approx(expected, rel=1e-7)


def test_dollar_fn_visible_through_let():
    assert render("let($fn = 64) cylinder(h = 10, r = 1);").volume() == pytest.approx(
        IDEAL_CYLINDER_10_1, rel=0.005
    )


def test_dollar_fn_on_a_builtin_reaches_its_children():
    # A documented divergence from OpenSCAD (see docs/QUIRKS.md): we let
    # `$`-arguments on builtin calls through to the children, so this is
    # fine-grained where OpenSCAD keeps the child at default resolution.
    source = "union($fn = 360) cylinder(h = 10, r = 1);"
    assert render(source).volume() == pytest.approx(IDEAL_CYLINDER_10_1, rel=0.001)


## =========================================================================
# difference() with tessellated parts


def test_blind_hole_leaves_material_above_it():
    # h=12 centered spans z in [-6, 6], so an h=10 outer cylinder keeps a
    # 4 mm solid cap on top: pi*(25*10 - 9*6) = 615.75, not the through-
    # hole 502.65. (An earlier version of this suite expected 502.65 and
    # "found" a 40% volume loss that was actually correct geometry.)
    result = render(
        """
        $fn = 64;
        difference() {
            cylinder(h = 10, r = 5);
            cylinder(h = 12, r = 3, center = true);
        }
        """
    )
    assert result.volume() == pytest.approx(math.pi * (25 * 10 - 9 * 6), rel=0.005)
    # Ring below the hole's ceiling, solid disc above it.
    assert result.slice(3).area() == pytest.approx(math.pi * 16, rel=0.01)
    assert result.slice(8).area() == pytest.approx(math.pi * 25, rel=0.01)


def test_through_hole_punches_the_full_height():
    result = render(
        """
        $fn = 64;
        difference() {
            cylinder(h = 10, r = 5);
            cylinder(h = 22, r = 3, center = true);
        }
        """
    )
    assert result.volume() == pytest.approx(math.pi * 16 * 10, rel=0.005)


## =========================================================================
# Tessellation leaves geometry sound


def test_explicit_counts_ignore_manifolds_global_settings():
    # manifold3d carries process-global tessellation defaults
    # (set_circular_segments & co). Our builtins always pass an explicit
    # fragment count, which the constructors must honor verbatim -- stray
    # global settings must not leak into a render.
    import manifold3d

    manifold3d.set_circular_segments(64)
    try:
        assert render("cylinder(h = 10, r = 1);").volume() == pytest.approx(PENTAGON_10_1)
    finally:
        manifold3d.set_circular_segments(0)  # 0 restores manifold's auto mode


@pytest.mark.parametrize(
    "source",
    [
        "cylinder(h = 10, r = 1, $fn = 3);",
        "cylinder(h = 10, r = 1, $fn = 64);",
        "cylinder(h = 10, r1 = 2, r2 = 0, $fn = 8);",
        "sphere(1, $fn = 4);",
        "sphere(1, $fn = 64);",
        "difference() { cylinder(h = 10, r = 2, $fn = 64); cylinder(h = 12, r = 1, $fn = 64, center = true); }",
    ],
)
def test_tessellated_results_are_valid_manifolds(source):
    result = render(source)
    assert result is not None
    assert result.volume() > 0
    assert result.num_vert() > 0
    assert result.genus() is not None
