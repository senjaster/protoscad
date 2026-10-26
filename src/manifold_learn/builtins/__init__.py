from typing import Protocol

from manifold_learn.builtins.cube import CubeModule
from manifold_learn.builtins.cylinder import CylinderModule
from manifold_learn.builtins.difference import DifferenceModule
from manifold_learn.builtins.hull import HullModule
from manifold_learn.builtins.intersection import IntersectionModule
from manifold_learn.builtins.let import LetModule
from manifold_learn.builtins.minkowski import MinkowskiModule
from manifold_learn.builtins.mirror import MirrorModule
from manifold_learn.builtins.rotate import RotateModule
from manifold_learn.builtins.scale import ScaleModule
from manifold_learn.builtins.sphere import SphereModule
from manifold_learn.builtins.translate import TranslateModule
from manifold_learn.builtins.union import UnionModule
from manifold_learn.runtime.module_definition import BuiltinModule


class BuiltinModuleFactory(Protocol):
    """A concrete ``BuiltinModule`` subclass, instantiable to a module."""

    def __call__(self) -> BuiltinModule: ...

__all__ = [
    "CubeModule",
    "CylinderModule",
    "DifferenceModule",
    "HullModule",
    "IntersectionModule",
    "LetModule",
    "MinkowskiModule",
    "MirrorModule",
    "RotateModule",
    "ScaleModule",
    "SphereModule",
    "TranslateModule",
    "UnionModule",
]

BUILTIN_MODULES: list[BuiltinModuleFactory] = [
    CubeModule,
    CylinderModule,
    DifferenceModule,
    HullModule,
    IntersectionModule,
    LetModule,
    MinkowskiModule,
    MirrorModule,
    RotateModule,
    ScaleModule,
    SphereModule,
    TranslateModule,
    UnionModule,
]
