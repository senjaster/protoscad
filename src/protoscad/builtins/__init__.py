from typing import Protocol

from protoscad.builtins.csg.difference import DifferenceModule
from protoscad.builtins.csg.hull import HullModule
from protoscad.builtins.csg.intersection import IntersectionModule
from protoscad.builtins.csg.minkowski import MinkowskiModule
from protoscad.builtins.csg.union import UnionModule
from protoscad.builtins.ext.metaballs import MetaballsModule
from protoscad.builtins.lang.conditional import IfModule
from protoscad.builtins.lang.let import LetModule
from protoscad.builtins.lang.loops import ForModule, IntersectionForModule
from protoscad.builtins.primitives.cube import CubeModule
from protoscad.builtins.primitives.cylinder import CylinderModule
from protoscad.builtins.primitives.sphere import SphereModule
from protoscad.builtins.transformations.mirror import MirrorModule
from protoscad.builtins.transformations.multmatrix import MultmatrixModule
from protoscad.builtins.transformations.resize import ResizeModule
from protoscad.builtins.transformations.rotate import RotateModule
from protoscad.builtins.transformations.scale import ScaleModule
from protoscad.builtins.transformations.translate import TranslateModule
from protoscad.builtins.utility.assertion import AssertModule
from protoscad.builtins.utility.echo import EchoModule
from protoscad.runtime.module_definition import BuiltinModule


class BuiltinModuleFactory(Protocol):
    """A concrete ``BuiltinModule`` subclass, instantiable to a module."""

    def __call__(self) -> BuiltinModule: ...


__all__ = [
    "AssertModule",
    "CubeModule",
    "CylinderModule",
    "DifferenceModule",
    "EchoModule",
    "ForModule",
    "HullModule",
    "IfModule",
    "IntersectionModule",
    "IntersectionForModule",
    "LetModule",
    "MetaballsModule",
    "MinkowskiModule",
    "MirrorModule",
    "MultmatrixModule",
    "ResizeModule",
    "RotateModule",
    "ScaleModule",
    "SphereModule",
    "TranslateModule",
    "UnionModule",
]

BUILTIN_MODULES: list[BuiltinModuleFactory] = [
    AssertModule,
    CubeModule,
    CylinderModule,
    DifferenceModule,
    EchoModule,
    ForModule,
    HullModule,
    IfModule,
    IntersectionModule,
    IntersectionForModule,
    LetModule,
    MetaballsModule,
    MinkowskiModule,
    MirrorModule,
    MultmatrixModule,
    ResizeModule,
    RotateModule,
    ScaleModule,
    SphereModule,
    TranslateModule,
    UnionModule,
]
