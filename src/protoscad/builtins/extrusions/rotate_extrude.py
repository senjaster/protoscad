from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.builtins._fragments import dollar_tessellation, fragments_from_radius
from protoscad.builtins._operations import child_profile
from protoscad.diagnostics import GeometryError
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, NumberLiteral


class RotateExtrudeModule(BuiltinModule):
    """``rotate_extrude`` — revolve 2D children into a solid of revolution.

    The profile's x is the radius, its y the future z (Manifold revolves
    around the 2D Y axis and stands the result up on Z, OpenSCAD's own
    convention). All points must sit on one side of the axis: a profile
    straddling it is an error; one entirely on the negative side is mirrored
    first — OpenSCAD revolves ``|x|`` there, Manifold only accepts the
    positive side. A partial ``angle`` (anything but 360) caps the sweep.
    """

    def instantiate(self, ctx: Invocation) -> Manifold | None:
        profile = child_profile(ctx, "rotate_extrude")
        if profile is None:
            return None

        angle = ctx.arg_values["angle"]
        # Out-of-range angles become a full turn, per OpenSCAD.
        if angle <= -360 or angle > 360:
            angle = 360
        if angle == 0:
            return None

        xs = [float(x) for contour in profile.to_polygons() for x in contour[:, 0]]
        min_x, max_x = min(xs), max(xs)
        if min_x < 0 < max_x:
            raise GeometryError("rotate_extrude() points must all have the same sign of x")
        if min_x < 0:
            profile = profile.scale((-1, 1))

        # The fragment budget of the profile's x span, taken proportionally
        # to the sweep: Manifold's segments cover the swept angle itself.
        fn, fs, fa = dollar_tessellation(ctx)
        fragments = fragments_from_radius(max_x - min_x, fn, fs, fa)
        segments = max(int(fragments * abs(angle) / 360), 1)

        solid = profile.revolve(segments, abs(angle))
        if angle < 0:
            # Revolving the other way is the mirror image of the sweep, and
            # Manifold would return an inside-out solid for negative degrees.
            solid = solid.mirror((0, 1, 0))
        return solid

    @property
    def name(self) -> str:
        return "rotate_extrude"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            optional={
                "angle": NumberLiteral(360),
                # Rendering hint, accepted for source compatibility.
                "convexity": NumberLiteral(2),
            }
        )
