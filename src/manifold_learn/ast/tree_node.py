from ast import List
from dataclasses import dataclass
from typing import Any, Sequence

from manifold_learn.ast.expression import Expression


@dataclass
class TreeNode:
    _parent: TreeNode | None
    _children: List[TreeNode]
    _variables: dict[str, Expression]  # Type to be defined
    _modules: dict[str, Any]

    def assign_variable(self, name: str, expression: Expression):
        self._variables[name] = expression

    def eval_variable(self, name: str) -> Any:
        if name in self._variables:

            return self._variables[name].evaluate(self)
        else:
            return self._parent.eval_variable(name) if self._parent else None

    def set_module(self, name: str, value: Any):
        self._modules[name] = value

    def get_module(self, name: str) -> Any:
        if name in self._modules:
            return self._modules[name]
        else:
            return self._parent.get_module(name) if self._parent else None

    @property
    def parent(self) -> 'TreeNode':
        return self._parent

    @property
    def children(self) -> Sequence[TreeNode]:
        # Conceal the fact it is mutable
        return self._children

    def add_child(self, child: 'TreeNode'):
        self._children.append(child)
        child._parent = self

    def remove_child(self, child: 'TreeNode'):
        self._children.remove(child)
        child._parent = None

