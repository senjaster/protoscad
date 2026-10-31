"""The 2D pipeline: ``square`` produces planar geometry (manifold
``CrossSection``), the shared operations keep it planar, and
``linear_extrude`` is what turns it into a solid."""

from __future__ import annotations

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
    with pytest.raises(Exception, match="linear_extrude.. extrudes 2D children"):
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
