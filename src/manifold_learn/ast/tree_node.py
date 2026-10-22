from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence
from copy import copy

from manifold_learn.ast.expression import Assignment, Expression
from manifold_learn.ast.module_definition import ModuleDefinition


@dataclass
class TreeNode:
    module: str  # Module name
    positional_args: list[Expression] = field(default_factory=list)
    named_args: dict[str, Expression] = field(default_factory=dict)
    _parent: TreeNode | None = None
    _children: list[TreeNode] = field(default_factory=list)
    _variables: dict[str, Assignment] = field(default_factory=dict)  # Type to be defined
    _modules: dict[str, ModuleDefinition] = field(default_factory=dict)

    def assign_variable(self, assignment: Assignment):
        self._variables[assignment.name] = assignment

    def excluding_var(self, name: str) -> "TreeNode":
        """Return a copy of this node that does not resolve ``name`` in its
        own scope, falling through to the parent instead.

        This prevents a variable definition from referencing itself: in
        ``{ width = width / 2; }`` the right-hand ``width`` resolves to the
        parent scope, per OpenSCAD's declarative semantics.
        """
        node = copy(self)
        node._variables = {k: v for k, v in self._variables.items() if k != name}
        return node

    def eval_variable(self, name: str) -> Any:
        """Resolve a variable in scope.

        Lookup order is: current scope first, then parent scope. The variable
        is stored as an Assignment expression, which excludes itself during
        evaluation so a definition cannot reference itself.
        """
        if name in self._variables:
            return self._variables[name].evaluate(self)
        if self._parent is not None:
            return self._parent.eval_variable(name)
        return None

    def set_module(self, name: str, value: ModuleDefinition):
        self._modules[name] = value

    def get_module(self, name: str) -> ModuleDefinition | None:
        if name in self._modules:
            return self._modules[name]
        else:
            return self._parent.get_module(name) if self._parent else None

    @property
    def parent(self) -> TreeNode | None:
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

    def make_parameter_scope(self, parameters: dict[str, Assignment]):
        """Create a new scope with the given parameters.

        Such scopes are used to evaluate the body of a module.
        """
        parameters = parameters or {}
        return TreeNode("scope", _parent=self, _variables=parameters)
