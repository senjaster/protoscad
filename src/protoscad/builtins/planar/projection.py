from __future__ import annotations

from collections.abc import Mapping

from manifold3d import CrossSection, FillRule, Manifold

from protoscad.builtins._operations import union_geometries
from protoscad.diagnostics import GeometryError
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, NumberLiteral


class ProjectionModule(BuiltinModule):
    """``projection`` — flatten 3D children onto the XY plane.

    ``cut = true`` takes the cross-section where the children meet z = 0;
    the default projects the whole solid to its shadow from above.
    """

    def instantiate(self, ctx: Invocation) -> CrossSection | None:
        solid = union_geometries(ctx.evaluate_children())
        if solid is None:
            return None
        if not isinstance(solid, Manifold):
            raise GeometryError("projection() projects 3D children")

        if bool(ctx.arg_values["cut"]):
            return solid.slice(0)
        # Manifold's projected outline may self-intersect where faces
        # overlap; the positive fill rule turns it into the shadow.
        return CrossSection(solid.project().to_polygons(), FillRule.Positive)

    @property
    def name(self) -> str:
        return "projection"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(optional={"cut": NumberLiteral(0), "convexity": NumberLiteral(2)})
