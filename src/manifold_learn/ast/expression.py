from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from manifold_learn.ast.tree_node import TreeNode


class Expression:
    def __init__(self, value):
        self.value = value

    def evaluate(self, node: "TreeNode") -> Any:
        return self.value