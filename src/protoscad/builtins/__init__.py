from typing import Protocol

from protoscad.builtins.conditional import IfModule
from protoscad.builtins.cube import CubeModule
from protoscad.builtins.cylinder import CylinderModule
from protoscad.builtins.difference import DifferenceModule
from protoscad.builtins.hull import HullModule
from protoscad.builtins.intersection import IntersectionModule
from protoscad.builtins.let import LetModule
from protoscad.builtins.loops import ForModule, IntersectionForModule
from protoscad.builtins.metaballs import MetaballsModule
from protoscad.builtins.minkowski import MinkowskiModule
from protoscad.builtins.mirror import MirrorModule
from protoscad.builtins.rotate import RotateModule
from protoscad.builtins.scale import ScaleModule
from protoscad.builtins.sphere import SphereModule
from protoscad.builtins.translate import TranslateModule
from protoscad.builtins.union import UnionModule
from protoscad.runtime.module_definition import BuiltinModule


class BuiltinModuleFactory(Protocol):
    """A concrete ``BuiltinModule`` subclass, instantiable to a module."""

    def __call__(self) -> BuiltinModule: ...


__all__ = [
    "CubeModule",
    "CylinderModule",
    "DifferenceModule",
    "ForModule",
    "HullModule",
    "IfModule",
    "IntersectionModule",
    "IntersectionForModule",
    "LetModule",
    "MetaballsModule",
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
    ForModule,
    HullModule,
    IfModule,
    IntersectionModule,
    IntersectionForModule,
    LetModule,
    MetaballsModule,
    MinkowskiModule,
    MirrorModule,
    RotateModule,
    ScaleModule,
    SphereModule,
    TranslateModule,
    UnionModule,
]
