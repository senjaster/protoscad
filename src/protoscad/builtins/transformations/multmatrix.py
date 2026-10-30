from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
from manifold3d import Manifold

from protoscad.builtins._operations import union_geometries
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment


class MultmatrixModule(BuiltinModule):
    def instantiate(self, ctx: Invocation) -> Manifold | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        m: Sequence[Sequence[float]] = ctx.arg_values["m"]
        # OpenSCAD's multmatrix is a 4x4 row-major matrix whose last row is
        # [0, 0, 0, 1]; Manifold's transform takes the 3x4 affine part (the
        # first three rows), with the last column being the translation.
        affine = np.array(m[:3], dtype=np.float64)
        return child.transform(affine)

    @property
    def name(self) -> str:
        return "multmatrix"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("m",))
