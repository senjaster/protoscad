from __future__ import annotations

from collections.abc import Mapping, Sequence

from manifold3d import CrossSection

from protoscad.builtins._operations import Geometry, union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment, NumberLiteral


def _scale_factors(newsize: Sequence[float], sizes: Sequence[float], auto: bool) -> list[float]:
    """Per-axis scale factors that resize the current sizes to newsize.

    A zero target leaves that axis unchanged unless ``auto`` is set, in
    which case it scales to preserve the aspect ratio.
    """
    scale: list[float] = []
    first_nonzero_scale: float | None = None
    for target, current in zip(newsize, sizes, strict=True):
        if target != 0:
            factor = target / current
            scale.append(factor)
            if first_nonzero_scale is None:
                first_nonzero_scale = factor
        else:
            scale.append((first_nonzero_scale or 1.0) if auto else 1.0)
    return scale


class ResizeModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Geometry | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        newsize: Sequence[float] = ctx.arg_values["newsize"]
        auto: bool = bool(ctx.arg_values["auto"])

        sizes: tuple[float, ...]
        if isinstance(child, CrossSection):
            # A plane sizes by its bounds; a z entry in newsize is dropped.
            xmin, ymin, xmax, ymax = child.bounds()
            sizes = (xmax - xmin, ymax - ymin)
            return child.scale(_scale_factors(newsize[:2], sizes, auto))

        xmin, ymin, zmin, xmax, ymax, zmax = child.bounding_box()
        sizes = (xmax - xmin, ymax - ymin, zmax - zmin)
        return child.scale(_scale_factors(newsize, sizes, auto))

    @property
    def name(self) -> str:
        return "resize"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("newsize",),
            optional={"auto": NumberLiteral(0)},
        )
