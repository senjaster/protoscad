from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection

from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, Literal, NumberLiteral


class PolygonModule(BuiltinModule):
    """``polygon(points, paths)`` — a custom shape from coordinates.

    Holes are wound the other way: the contours fill by winding rule (the
    same convention OpenSCAD's Clipper pipeline resolves by), so an outer
    loop and an oppositely-wound inner loop make a ring. ``paths`` selects
    and orders point indices into contours; without it the points are one
    single contour.
    """

    def instantiate(self, ctx: Invocation) -> CrossSection:
        points = ctx.arg_values["points"]
        paths = ctx.arg_values["paths"]

        vertices = []
        for index, point in enumerate(points):
            if not isinstance(point, list) or len(point) < 2:
                raise ProtoSCADError(
                    f"polygon() points[{index}] is not an [x, y] pair",
                    code=ErrorCode.INVALID_ARGUMENT,
                    span=ctx.node.span,
                )
            vertices.append([point[0], point[1]])

        if not paths:
            # No paths (or an empty list): all points form the one contour.
            contours = [vertices]
        else:
            contours = []
            for path in paths:
                contour = []
                for index in path:
                    # Point indices are numbers in the language's type
                    # system; OpenSCAD truncates them the same way.
                    idx = int(index)
                    if not 0 <= idx < len(vertices):
                        raise ProtoSCADError(
                            f"polygon() point index {idx} is out of bounds",
                            code=ErrorCode.INVALID_ARGUMENT,
                            span=ctx.node.span,
                        )
                    contour.append(vertices[idx])
                contours.append(contour)

        # Degenerate contours (<3 vertices) enclose nothing; OpenSCAD's
        # sanitizer drops them too.
        contours = [contour for contour in contours if len(contour) >= 3]
        return CrossSection(contours)

    @property
    def name(self) -> str:
        return "polygon"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("points",),
            optional={"paths": Literal(None), "convexity": NumberLiteral(1)},  # rendering hint, ignored
        )
