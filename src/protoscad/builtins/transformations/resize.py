from __future__ import annotations

from collections.abc import Mapping, Sequence

from manifold3d import Manifold

from protoscad.builtins._operations import union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, NumberLiteral


class ResizeModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Manifold | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        newsize: Sequence[float] = ctx.arg_values["newsize"]
        auto: bool = bool(ctx.arg_values["auto"])

        xmin, ymin, zmin, xmax, ymax, zmax = child.bounding_box()
        sizes = (xmax - xmin, ymax - ymin, zmax - zmin)

        scale: list[float] = []
        first_nonzero_scale: float | None = None
        for target, current in zip(newsize, sizes, strict=True):
            if target != 0:
                factor = target / current
                scale.append(factor)
                if first_nonzero_scale is None:
                    first_nonzero_scale = factor
            else:
                # A zero target leaves that axis unchanged unless auto is set,
                # in which case it scales to preserve the aspect ratio.
                scale.append((first_nonzero_scale or 1.0) if auto else 1.0)

        return child.scale(scale)

    @property
    def name(self) -> str:
        return "resize"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("newsize",),
            optional={"auto": NumberLiteral(0)},
        )
