from typing import Generic, Mapping, Sequence

from manifold_learn.ast.expression import Assignment
from manifold_learn.ast.module_definition import ModuleDefinition, Geometry
from manifold_learn.ast.tree_node import TreeNode


class UserDefinedModule(ModuleDefinition, Generic[Geometry]):

    def __init__(self, name: str, parameters: Mapping[str, Assignment], body: TreeNode):
        self._name = name
        self._parameters = parameters
        self.body = body

    def eval(self, scope: TreeNode, children: Sequence[Geometry]) -> Geometry:
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self._parameters