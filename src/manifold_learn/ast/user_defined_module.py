from typing import Generic, Mapping

from manifold_learn.ast.expression import Assignment
from manifold_learn.ast.module_definition import EvalContext, Geometry, ModuleDefinition
from manifold_learn.ast.tree_node import TreeNode


class UserDefinedModule(ModuleDefinition, Generic[Geometry]):

    def __init__(self, name: str, parameters: Mapping[str, Assignment], body: TreeNode):
        self._name = name
        self._parameters = parameters
        self.body = body

    def instantiate(self, ctx: EvalContext) -> Geometry | list[Geometry] | None:
        # Instantiating the body in its definition-site environment is what
        # statement kinds (#3) will wire up; unreachable until then.
        return None

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self._parameters