from __future__ import annotations

from collections.abc import Sequence

from manifold3d import CrossSection, Manifold, OpType

from protoscad.diagnostics import GeometryError

#: What a module's ``instantiate`` hands to its parent: a solid (``Manifold``)
#: or a planar region (``CrossSection``). 2D geometry flows through the same
#: tree as 3D — transforms and booleans dispatch on the kind, and an
#: extrusion is what turns one into the other.
type Geometry = Manifold | CrossSection

_OPERATION_NAMES = {OpType.Add: "union", OpType.Subtract: "difference", OpType.Intersect: "intersection"}


def union_geometries(geometries: Sequence[Geometry]) -> Geometry | None:
    """Implicit union: what a scope with several instantiations produces."""
    return boolean_geometries(geometries, OpType.Add)


def boolean_geometries(geometries: Sequence[Geometry], op: OpType) -> Geometry | None:
    """Apply a boolean operation across a non-empty sequence of geometries.

    2D children boolean among themselves, so a 2D subtree stays 2D until an
    extrusion consumes it. Mixing the two dimensions in one operation raises
    ``GeometryError`` — reported without a location here and located at the
    enclosing call by ``Invocation`` — where OpenSCAD warns and silently
    drops the minority kind.
    """
    if not geometries:
        return None
    planar = [geometry for geometry in geometries if isinstance(geometry, CrossSection)]
    if planar:
        if len(planar) != len(geometries):
            raise GeometryError(f"Cannot combine 2D and 3D children in '{_OPERATION_NAMES[op]}'")
        if len(planar) == 1:
            return planar[0]
        return CrossSection.batch_boolean(planar, op)
    if len(geometries) == 1:
        return geometries[0]
    return Manifold.batch_boolean(list(geometries), op)


def xy_pair(v: float | list[float]) -> tuple[float, float]:
    """The XY components of a transform argument applied to 2D geometry: a
    vector keeps its first two entries (z is dropped — a plane has none), a
    scalar is taken uniformly."""
    if isinstance(v, list):
        return (v[0], v[1])
    return (v, v)
