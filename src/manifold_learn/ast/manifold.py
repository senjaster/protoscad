from typing import Mapping, Sequence, Any

from manifold3d import Manifold, OpType

from manifold_learn.ast.expression import Assignment, NumberLiteral
from manifold_learn.ast.module_definition import BuiltinModule, ModuleDefinition, Geometry
from manifold_learn.ast.tree_node import TreeNode


class IdentityModule(ModuleDefinition[Manifold]):

    def __init__(self, name: str):
        self._name = name

    def eval(self, scope: TreeNode, children: Sequence[Geometry]) -> Geometry:
        if len(children) == 1:
            return children[0]
        elif len(children) == 0:
            return None
        return Manifold.batch_boolean(children, OpType.Add)

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}


class CubeModule(BuiltinModule[Manifold]):
    def eval(self, arguments: dict[str, Any], children: Sequence[Geometry]) -> Manifold:
        size = arguments["size"]
        if not isinstance(size, list):
            size = [size, size, size]
        center = bool(arguments["center"])
        return Manifold.cube(size, center)

    @property
    def name(self) -> str:
        return "cube"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("size",),
            optional={"center": NumberLiteral(0)},
        )

class TranslateModule(BuiltinModule[Manifold]):
    def eval(self, arguments: dict[str, Any], children: Sequence[Manifold]) -> Manifold:
        if len(children) > 1:
            raise ValueError("translate module must have exactly one child")
        elif len(children) == 0:
            return None

        child = children[0]
        offset = arguments["offset"]
        return child.translate(offset)

    @property
    def name(self) -> str:
        return "translate"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("offset",))