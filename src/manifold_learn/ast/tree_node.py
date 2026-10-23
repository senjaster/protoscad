from __future__ import annotations

from dataclasses import dataclass, field

from manifold_learn.ast.expression import Assignment, Expression
from manifold_learn.ast.module_definition import ModuleDefinitionNode


@dataclass
class TreeNode:
    """A module call in the AST, as pure data.

    Scope resolution does not flow through the tree: the ``variables`` and
    ``modules`` registered here are declarative data that the evaluator turns
    into an ``Environment`` when it instantiates the node.
    """

    module: str  # Module name
    positional_args: list[Expression] = field(default_factory=list)
    named_args: dict[str, Expression] = field(default_factory=dict)
    variables: dict[str, Assignment] = field(default_factory=dict)
    modules: dict[str, ModuleDefinitionNode] = field(default_factory=dict)
    children: list[TreeNode] = field(default_factory=list)
    parent: TreeNode | None = field(default=None, repr=False)

    def assign_variable(self, assignment: Assignment) -> None:
        self.variables[assignment.name] = assignment

    def define_module(self, definition: ModuleDefinitionNode) -> None:
        self.modules[definition.name] = definition

    def add_child(self, child: TreeNode) -> None:
        self.children.append(child)
        child.parent = self
