from __future__ import annotations

from collections.abc import Mapping

from manifold3d import Manifold

from protoscad.builtins._fragments import tessellation_for
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, Literal, NumberLiteral


class SphereModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Manifold:
        diameter = ctx.arg_values["d"]
        radius = ctx.arg_values["r"]
        if diameter is not None:
            radius = diameter / 2
        # Manifold builds spheres by refining a tetrahedron rather than
        # revolving a circle; the fragment count only steers how fine that
        # refinement gets, which keeps our meshes manifold's shape while
        # honoring OpenSCAD's $fn/$fa/$fs resolution knobs.
        return Manifold.sphere(radius, tessellation_for(ctx, radius))

    @property
    def name(self) -> str:
        return "sphere"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            optional={"r": NumberLiteral(1), "d": Literal(None)},
        )
