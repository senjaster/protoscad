"""The 2D pipeline: ``square`` produces planar geometry (manifold
``CrossSection``), the shared operations keep it planar, and
``linear_extrude`` is what turns it into a solid."""

from __future__ import annotations

import math

import pytest
from manifold3d import CrossSection, Manifold

from protoscad.builtins import BUILTIN_MODULES
from protoscad.diagnostics import ErrorCode, ProtoSCADError, SourceSpan
from protoscad.parser import parse_scad
from protoscad.render import crosssection2path
from protoscad.runtime.evaluator import evaluate


def render(source: str):
    return evaluate(parse_scad(source), (factory() for factory in BUILTIN_MODULES))


## =========================================================================
# square


def test_square_is_a_cross_section_with_area_and_bounds():
    result = render("square(5);")
    assert isinstance(result, CrossSection)
    assert result.bounds() == pytest.approx((0, 0, 5, 5))
    assert result.area() == pytest.approx(25)


def test_square_vector_size_and_center():
    assert render("square([2, 3]);").bounds() == pytest.approx((0, 0, 2, 3))
    assert render("square([2, 3], center = true);").bounds() == pytest.approx((-1, -1.5, 1, 1.5))


## =========================================================================
# 2D children flow through the shared operations


def test_implicit_union_of_2d_children_stays_2d():
    result = render("union() { square(5); translate([10, 0]) square(5); }")
    assert isinstance(result, CrossSection)
    assert result.bounds() == pytest.approx((0, 0, 15, 5))
    assert result.area() == pytest.approx(50)


def test_2d_difference_and_intersection():
    assert render("difference() { square(10, center = true); square(5, center = true); }").area() == pytest.approx(75)
    assert render("intersection() { square(10); square([5, 20]); }").area() == pytest.approx(50)


def test_2d_geometry_through_for_and_let_scopes():
    looped = render("for (i = [0:2]) translate([i * 10, 0]) square(5);")
    assert isinstance(looped, CrossSection)
    assert looped.bounds() == pytest.approx((0, 0, 25, 5))
    assert looped.area() == pytest.approx(75)

    scoped = render("let (s = 5) square(s);")
    assert isinstance(scoped, CrossSection)
    assert scoped.area() == pytest.approx(25)


@pytest.mark.parametrize(
    ("source", "expected_bounds"),
    [
        ("translate([10, 0]) square(5);", (10, 0, 15, 5)),
        # A z offset on a plane child is dropped, not an error.
        ("translate([10, 0, 7]) square(5);", (10, 0, 15, 5)),
        ("translate(10) square(5);", (10, 10, 15, 15)),
        ("rotate(90) square(5);", (-5, 0, 0, 5)),
        ("rotate([0, 0, 90]) square(5);", (-5, 0, 0, 5)),
        # An x/y rotation leaves the plane; only the z entry applies.
        ("rotate([30, 45, 90]) square(5);", (-5, 0, 0, 5)),
        ("scale([2, 3]) square(5);", (0, 0, 10, 15)),
        ("scale(2) square(5);", (0, 0, 10, 10)),
        ("mirror([1, 0]) square(5);", (-5, 0, 0, 5)),
    ],
)
def test_transforms_on_2d_children(source, expected_bounds):
    assert render(source).bounds() == pytest.approx(expected_bounds)


def test_2d_transform_chain_matches_the_3d_semantics():
    result = render("translate([10, 0]) rotate(90) square(5);")
    assert result.bounds() == pytest.approx((5, 0, 10, 5))


## =========================================================================
# Mixing dimensions is an error


@pytest.mark.parametrize(
    "source",
    [
        "union() { cube(1); square(1); }",
        "difference() { square(10); cube(1); }",
        "intersection() { square(10); cube(1); }",
        # The mixed union fires inside the transform, locating the union.
        "translate([1, 2, 3]) union() { square(1); cube(1); }",
        "for (i = [0:1]) square(1); cube(1);",
    ],
)
def test_mixed_2d_3d_children_error(source):
    with pytest.raises(Exception, match="Cannot combine 2D and 3D children"):
        render(source)


@pytest.mark.parametrize(
    "source",
    [
        "linear_extrude(5) cube(1);",
        "linear_extrude(5) { square(2); cube(1); }",
    ],
)
def test_linear_extrude_rejects_3d_children(source):
    with pytest.raises(Exception, match="linear_extrude.. takes 2D children"):
        render(source)


def test_mixed_children_error_points_at_the_operation_call():
    # The geometry helpers raise unlocated errors; the innermost module
    # call whose body raised — the union on line 3, not the translate
    # above it — is the span Invocation attaches. A call's span is its
    # header, from `union` to the closing paren.
    source = "cube(1);\ntranslate([5, 0, 0])\nunion() {\n    square(1);\n    cube(1);\n}\n"
    with pytest.raises(ProtoSCADError) as excinfo:
        render(source)
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.TYPE_ERROR
    assert diagnostic.message == "Cannot combine 2D and 3D children in 'union'"
    assert diagnostic.span == SourceSpan(3, 0, 3, 7)


def test_linear_extrude_3d_child_error_points_at_the_extrude_call():
    source = "cube(1);\nlinear_extrude(5)\ncube(1);\n"
    with pytest.raises(ProtoSCADError) as excinfo:
        render(source)
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.TYPE_ERROR
    assert diagnostic.span == SourceSpan(2, 0, 2, 17)


## =========================================================================
# linear_extrude


def test_linear_extrude_makes_a_solid():
    result = render("linear_extrude(10) square(5);")
    assert isinstance(result, Manifold)
    assert result.volume() == pytest.approx(250)
    assert result.bounding_box() == pytest.approx((0, 0, 0, 5, 5, 10))


def test_linear_extrude_defaults_and_center():
    # OpenSCAD's height default is 100.
    assert render("linear_extrude() square(5);").bounding_box() == pytest.approx((0, 0, 0, 5, 5, 100))
    centered = render("linear_extrude(height = 10, center = true) square(5);")
    assert centered.bounding_box() == pytest.approx((0, 0, -5, 5, 5, 5))


def test_linear_extrude_unions_its_2d_children_first():
    result = render("linear_extrude(3) { square(4); translate([10, 0]) square(4); }")
    assert result.volume() == pytest.approx(96)


@pytest.mark.parametrize(
    "source",
    [
        "linear_extrude(0) square(5);",
        "linear_extrude(-10) square(5);",
        "linear_extrude(5);",
    ],
)
def test_linear_extrude_empty_results(source):
    # A non-positive height drops the whole node, as in OpenSCAD; no
    # children is no geometry.
    assert render(source) is None


def test_linear_extrude_scale_tapers_the_top():
    # A uniform scale halves both dimensions: frustum volume
    # h/3 * (A + a + sqrt(A*a)). A per-axis scale shrinks the area
    # linearly, so the plain prismatoid integral applies.
    assert render("linear_extrude(10, scale = 0.5) square(5);").volume() == pytest.approx(25 * 1.75 / 3 * 10)
    assert render("linear_extrude(10, scale = [1, 0.5]) square(5);").volume() == pytest.approx(187.5)


def test_linear_extrude_scale_zero_is_a_pyramid():
    assert render("linear_extrude(10, scale = 0) square(10);").volume() == pytest.approx(1000 / 3)


def test_linear_extrude_negative_scale_clamps_to_zero():
    assert render("linear_extrude(10, scale = -1) square(10);").volume() == pytest.approx(
        render("linear_extrude(10, scale = 0) square(10);").volume()
    )


def test_linear_extrude_twist_slices_follow_the_openscad_budgets():
    # The default count for this shape is 8 slices (see test_fragments);
    # the explicit same-count call must produce the identical mesh, and a
    # coarser count a different one.
    default = render("linear_extrude(10, twist = 90) square(5);").volume()
    assert default == pytest.approx(render("linear_extrude(10, twist = 90, slices = 8) square(5);").volume())
    assert default != pytest.approx(render("linear_extrude(10, twist = 90, slices = 3) square(5);").volume())
    # $fn slices by angle proportion: ceil(90/360 * 12) = 3.
    assert render("linear_extrude(10, twist = 90, $fn = 12) square(5);").volume() == pytest.approx(
        render("linear_extrude(10, twist = 90, slices = 3) square(5);").volume()
    )


def test_linear_extrude_twist_without_scaling_preserves_volume_per_slice():
    # One slice twists the corners in place — the volume of the box.
    assert render("linear_extrude(10, twist = 90, slices = 1) square(5);").volume() == pytest.approx(250)


def test_linear_extrude_accepts_convexity():
    # A rendering hint in OpenSCAD; accepted and ignored here.
    assert render("linear_extrude(10, convexity = 5) square(5);").volume() == pytest.approx(250)


def test_linear_extrude_of_a_2d_difference():
    result = render("linear_extrude(2) difference() { square(10, center = true); square(5, center = true); }")
    assert result.volume() == pytest.approx(150)


## =========================================================================
# 2D at the render boundary: vector export


def test_crosssection2path_closes_each_contour():
    section = render("union() { square(5); translate([10, 0]) square(5); }")
    path = crosssection2path(section)
    # Two contours, each closed back onto its first vertex, sharing one
    # vertex array: the shape the SVG/DXF exporters serialize.
    assert len(path.entities) == 2
    assert len(path.vertices) == 8
    for entity in path.entities:
        assert entity.points[0] == entity.points[-1]


## =========================================================================
# circle


def polygon_area(fragments: int, radius: float = 1.0) -> float:
    return fragments / 2 * radius**2 * math.sin(2 * math.pi / fragments)


def test_circle_default_is_the_openscad_pentagon():
    result = render("circle(1);")
    assert isinstance(result, CrossSection)
    assert result.area() == pytest.approx(polygon_area(5))
    # Vertices start at angle 0 and step 72 degrees, so the bounds are the
    # extreme vertices: x from 144/0 degrees, y from 288/72 degrees.
    expected = (math.cos(math.radians(144)), math.sin(math.radians(288)), 1, math.sin(math.radians(72)))
    assert result.bounds() == pytest.approx(expected)


@pytest.mark.parametrize(
    ("source", "fragments"),
    [
        ("circle($fn = 6);", 6),
        ("circle($fn = 3);", 3),
        ("circle(r = 2, $fn = 8);", 8),
        ("circle(d = 2, $fn = 8);", 8),
        # The default budgets ($fa=12, $fs=2): the $fs arc budget gives 7,
        # and $fa caps a larger radius at 30.
        ("circle(r = 2);", 7),
        ("circle(r = 10);", 30),
    ],
)
def test_circle_fragment_counts_follow_the_budgets(source, fragments):
    assert render(source).area() == pytest.approx(polygon_area(fragments, radius=render(source).bounds()[2]))


def test_circle_nonpositive_radius_is_empty():
    assert render("circle(0);").is_empty()


## =========================================================================
# polygon


def test_polygon_single_contour_is_all_points():
    result = render("polygon([[0, 0], [10, 0], [0, 10]]);")
    assert result.area() == pytest.approx(50)
    assert result.bounds() == pytest.approx((0, 0, 10, 10))


def test_polygon_paths_select_points_into_contours():
    # One square split across two same-wound triangular paths: the two
    # contours union back into the square.
    result = render("polygon([[0, 0], [10, 0], [10, 10], [0, 10]], [[0, 1, 2], [0, 2, 3]]);")
    assert result.area() == pytest.approx(100)


def test_polygon_hole_is_the_oppositely_wound_path():
    source = (
        "polygon(points = [[0, 0], [10, 0], [10, 10], [0, 10], [3, 3], [7, 3], [7, 7], [3, 7]],"
        " paths = [[0, 1, 2, 3], [7, 6, 5, 4]]);"
    )
    assert render(source).area() == pytest.approx(100 - 16)
    # The same inner path wound like the outer is no hole at all.
    same_winding = source.replace("[7, 6, 5, 4]", "[4, 5, 6, 7]")
    assert render(same_winding).area() == pytest.approx(100)


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("polygon([[0, 0], [1]]);", "not an .x, y. pair"),
        ("polygon([[0, 0], [1, 1]], [[0, 5]]);", "index 5 is out of bounds"),
    ],
)
def test_polygon_rejects_malformed_arguments(source, message):
    with pytest.raises(ProtoSCADError, match=message):
        render(source)


## =========================================================================
# offset


def test_offset_delta_miters_the_corners_exactly():
    assert render("offset(delta = 2) square(10);").area() == pytest.approx(196)
    assert render("offset(delta = 2) square(10);").bounds() == pytest.approx((-2, -2, 12, 12))


def test_offset_delta_chamfer_cuts_the_corners():
    # Each 90-degree corner is cut at 45 degrees instead of kept sharp.
    assert render("offset(delta = 2, chamfer = true) square(10);").area() == pytest.approx(193.2548, abs=1e-3)


def test_offset_r_rounds_the_corners_by_the_fragment_budgets():
    # Growing a 10x10 square by r=2 is its Minkowski sum with a disc:
    # 100 + perimeter*r + pi*r^2 in the limit of fine $fn.
    fine = render("offset(r = 2, $fn = 200) square(10);")
    assert fine.area() == pytest.approx(100 + 40 * 2 + math.pi * 4, rel=0.01)
    assert fine.bounds() == pytest.approx((-2, -2, 12, 12))
    # At the default budgets the arcs are coarse (7 segments), so less.
    assert render("offset(r = 2) square(10);").area() < fine.area()


def test_offset_default_is_round_r_1():
    assert render("offset() square(10);").area() == pytest.approx(render("offset(r = 1) square(10);").area())


def test_offset_negative_shrinks():
    assert render("offset(r = -2) square(10);").area() == pytest.approx(36)


def test_offset_r_wins_over_delta():
    # r rounds; the delta is the same magnitude either way here.
    assert render("offset(r = 2, delta = 2) square(10);").area() == pytest.approx(
        render("offset(r = 2) square(10);").area()
    )


def test_offset_takes_only_2d_children():
    with pytest.raises(ProtoSCADError, match="offset.. takes 2D children"):
        render("offset(2) cube(1);")


## =========================================================================
# rotate_extrude


def test_rotate_extrude_full_torus():
    torus = render("rotate_extrude($fn = 96) translate([10, 0]) circle(1, $fn = 48);")
    assert torus.volume() == pytest.approx(2 * math.pi**2 * 10, rel=0.01)


def test_rotate_extrude_partial_and_negative_angles():
    full = render("rotate_extrude($fn = 96) translate([10, 0]) circle(1, $fn = 48);").volume()
    quarter = render("rotate_extrude(angle = 90, $fn = 96) translate([10, 0]) circle(1, $fn = 48);").volume()
    assert quarter == pytest.approx(full / 4, rel=0.01)
    # Revolving the other way is the mirror image: same volume.
    mirrored = render("rotate_extrude(angle = -90, $fn = 96) translate([10, 0]) circle(1, $fn = 48);").volume()
    assert mirrored == pytest.approx(quarter)


def test_rotate_extrude_angle_edges():
    # Zero degrees make no geometry; out-of-range becomes a full turn.
    assert render("rotate_extrude(angle = 0) square(5);") is None
    clamped = render("rotate_extrude(angle = 400, $fn = 96) translate([10, 0]) circle(1, $fn = 48);").volume()
    assert clamped == pytest.approx(render("rotate_extrude($fn = 96) translate([10, 0]) circle(1, $fn = 48);").volume())


def test_rotate_extrude_profile_touching_the_axis_is_fine():
    # A square at the origin revolves into a cylinder, not an error: only
    # straddling the axis is invalid.
    result = render("rotate_extrude($fn = 32) square([5, 2]);")
    assert result.volume() == pytest.approx(polygon_area(32, radius=5) * 2, rel=1e-6)
    assert result.bounding_box()[2:] == pytest.approx((0, 5, 5, 2))


def test_rotate_extrude_negative_x_profile_is_revolved_by_magnitude():
    positive = render("rotate_extrude($fn = 64) translate([10, 0]) circle(1, $fn = 32);").volume()
    negative = render("rotate_extrude($fn = 64) translate([-10, 0]) circle(1, $fn = 32);").volume()
    assert negative == pytest.approx(positive)


def test_rotate_extrude_rejects_profile_straddling_the_axis():
    with pytest.raises(ProtoSCADError, match="same sign of x"):
        render("rotate_extrude() translate([-1, 0]) square(5);")


def test_rotate_extrude_takes_only_2d_children():
    with pytest.raises(ProtoSCADError, match="rotate_extrude.. takes 2D children"):
        render("rotate_extrude() cube(1);")


## =========================================================================
# projection


def test_projection_cut_slices_at_z_zero():
    assert render("projection(cut = true) cube(2);").area() == pytest.approx(4)
    # Nothing meets z = 0: an empty section, not an error.
    assert render("projection(cut = true) translate([0, 0, 5]) cube(2);").is_empty()


def test_projection_shadow_is_the_union_along_z():
    stacked = render("projection() { cube([2, 2, 1]); translate([1, 1, 1]) cube([2, 2, 1]); }")
    assert stacked.bounds() == pytest.approx((0, 0, 3, 3))


def test_projection_takes_only_3d_children():
    with pytest.raises(ProtoSCADError, match="projection.. projects 3D children"):
        render("projection() square(2);")


## =========================================================================
# 2D-aware hull / resize / multmatrix


def test_2d_hull():
    result = render("hull() { square(5); translate([10, 0]) square(5); }")
    assert isinstance(result, CrossSection)
    assert result.area() == pytest.approx(75)
    # A hull preserves a convex child unchanged.
    assert render("hull() square(5);").area() == pytest.approx(25)


def test_hull_rejects_mixed_children():
    with pytest.raises(ProtoSCADError, match="Cannot combine 2D and 3D children in 'hull'"):
        render("hull() { square(1); cube(1); }")


def test_2d_resize():
    assert render("resize([10, 20]) square(5);").area() == pytest.approx(200)
    # A z entry sizes nothing on a plane.
    assert render("resize([10, 20, 999]) square(5);").area() == pytest.approx(200)
    # A zero target keeps the axis; auto scales it along.
    assert render("resize([10, 0]) square(5);").bounds() == pytest.approx((0, 0, 10, 5))
    assert render("resize([10, 0], auto = true) square(5);").area() == pytest.approx(100)


def test_2d_multmatrix():
    matrix = "multmatrix([[1, 0, 0, 3], [0, 1, 0, 4], [0, 0, 1, 0], [0, 0, 0, 1]])"
    assert render(f"{matrix} square(2);").bounds() == pytest.approx((3, 4, 5, 6))
    # The in-plane part of a rotation about z turns the square.
    rot = "multmatrix([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])"
    assert render(f"{rot} square(5);").bounds() == pytest.approx((-5, 0, 0, 5))
