from dataclasses import dataclass, field
from typing import Any, Sequence

from manifold_learn.ast.expression import Expression


@dataclass
class TreeNode:
    module: str  # Module name
    positional_args: list[Expression]
    named_args: dict[str, Expression]
    _parent: TreeNode | None = None
    _children: list[TreeNode] = field(default_factory=list)
    _variables: dict[str, Expression] = field(default_factory=dict)  # Type to be defined
    _modules: dict[str, Any] = field(default_factory=dict)

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

