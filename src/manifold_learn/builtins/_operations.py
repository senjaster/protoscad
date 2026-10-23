from __future__ import annotations

from collections.abc import Sequence

from manifold3d import Manifold, OpType


def union_geometries(geometries: Sequence[Manifold]) -> Manifold | None:
    """Implicit union: what a scope with several instantiations produces."""
    if not geometries:
        return None
    if len(geometries) == 1:
        return geometries[0]
    return Manifold.batch_boolean(list(geometries), OpType.Add)


def boolean_geometries(geometries: Sequence[Manifold], op: OpType) -> Manifold | None:
    """Apply a boolean operation across a non-empty sequence of geometries."""
    if not geometries:
        return None
    if len(geometries) == 1:
        return geometries[0]
    return Manifold.batch_boolean(list(geometries), op)
