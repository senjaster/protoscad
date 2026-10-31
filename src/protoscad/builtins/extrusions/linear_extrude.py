from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection, Manifold

from protoscad.builtins._fragments import dollar_tessellation, extrusion_slices
from protoscad.builtins._operations import child_profile
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, NumberLiteral


class LinearExtrudeModule(BuiltinModule):
    """``linear_extrude`` — sweep the union of 2D children into a solid.

    The children union in the plane first (a multi-child call extrudes one
    profile, not each child on its own), then Manifold extrudes it, laying
    ``slices`` copies between bottom and top with twist and scale
    interpolated linearly across them — the same construction OpenSCAD uses,
    which is why its slice-count rules (``_fragments.extrusion_slices``)
    port over directly.
    """

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        section = child_profile(ctx, "linear_extrude")
        if section is None:
            return None

        height = ctx.arg_values["height"]
        if height <= 0:
            # OpenSCAD drops the whole node for a non-positive height.
            return None

        twist = ctx.arg_values["twist"]
        scale = ctx.arg_values["scale"]
        if not isinstance(scale, list):
            scale = [scale, scale]
        elif len(scale) < 2:
            scale = scale * 2
        # Negative scale collapses to zero — a point at the top, per OpenSCAD.
        scale_x, scale_y = (max(component, 0.0) for component in scale[:2])

        slices = int(ctx.arg_values["slices"])
        if slices <= 0:
            # Without an explicit count, OpenSCAD slices finely enough that
            # a vertex's path (a helix under twist, a spiral under uniform
            # twist+scale, a diagonal under bare non-uniform scale) stays
            # within the $fa/$fs budgets.
            fn, fs, fa = dollar_tessellation(ctx)
            radius_sqr, delta_sqr = _vertex_path_extents(section, scale_x, scale_y)
            slices = extrusion_slices(radius_sqr, delta_sqr, height, twist, scale_x, scale_y, fn, fs, fa)

        # OpenSCAD's ``slices`` counts the bottom-to-top segments; Manifold's
        # ``n_divisions`` the extra vertex rings in between — one fewer.
        solid = section.extrude(height, n_divisions=slices - 1, twist_degrees=twist, scale_top=(scale_x, scale_y))
        if bool(ctx.arg_values["center"]):
            solid = solid.translate((0.0, 0.0, -height / 2))
        return solid

    @property
    def name(self) -> str:
        return "linear_extrude"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            optional={
                "height": NumberLiteral(100),
                "center": NumberLiteral(0),
                # OpenSCAD's rendering hint; kept for source compatibility,
                # no effect on the geometry.
                "convexity": NumberLiteral(2),
                "twist": NumberLiteral(0),
                "slices": NumberLiteral(0),
                "scale": NumberLiteral(1),
            }
        )


def _vertex_path_extents(section: CrossSection, scale_x: float, scale_y: float) -> tuple[float, float]:
    """How far the profile's vertices reach from the z axis, and how far the
    top scale carries them (both squared) — the inputs the slice rules put
    on the $fs budget."""
    radius_sqr = 0.0
    delta_sqr = 0.0
    for contour in section.to_polygons():
        for x, y in contour:
            radius_sqr = max(radius_sqr, x * x + y * y)
            dx = x * (1.0 - scale_x)
            dy = y * (1.0 - scale_y)
            delta_sqr = max(delta_sqr, dx * dx + dy * dy)
    return radius_sqr, delta_sqr
