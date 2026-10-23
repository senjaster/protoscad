from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from manifold_learn.ast.environment import Environment
from manifold_learn.ast.manifold import UnionModule
from manifold_learn.ast.module_definition import ChildInvocation, EvalContext, ModuleDefinition
from manifold_learn.ast.tree_node import TreeNode
from manifold_learn.ast.user_defined_module import UserDefinedModule


class TreeEvaluator:
    def __init__(self, builtin_modules: Iterable[ModuleDefinition]):
        union = UnionModule()
        self._modules: dict[str, ModuleDefinition] = {m.name: m for m in builtin_modules}
        # "root", "block" and "let" are internal aliases for the implicit
        # union, registered below the environment chain so a user module of
        # the same name shadows them. They exist only until the AST gets
        # real statement kinds.
        for name in ("union", "root", "block", "let"):
            self._modules.setdefault(name, union)

    def evaluate(self, root: TreeNode) -> Any:
        env = Environment(modules=self._modules)
        return self._instantiate(ChildInvocation(root, env))

    def _instantiate(self, invocation: ChildInvocation) -> Any:
        node = invocation.node
        env = invocation.env

        # Resolve the node's own module in the caller's scope, not in the
        # scope this node itself introduces: a node's variables/modules apply
        # to its children, not to its own resolution.
        module_def = env.lookup_module(node.module)
        if module_def is None:
            raise ValueError(f"Unknown module: {node.module!r}")

        # Build the scope visible to this node's arguments and children.
        scope_env = env
        if node.variables:
            scope_env = scope_env.extend(node.variables)
        if node.modules:
            # Turn each module definition into a UserDefinedModule bound to
            # this scope, so its body resolves surrounding names lexically.
            # The dynamic chain is inherited unchanged (nesting does not
            # cross a module boundary).
            modules = {
                name: UserDefinedModule(defn.name, defn.parameters, defn.body, scope_env)
                for name, defn in node.modules.items()
            }
            scope_env = Environment(modules=modules, parent=scope_env, dynamic_parent=scope_env._dynamic_parent)

        bound = module_def.bind_parameters(node.positional_args, node.named_args)
        # Arguments are evaluated in the caller's scope, not in the scope this
        # node introduces for its children.
        args = {name: assignment.value.evaluate(env) for name, assignment in bound.items()}
        children = self._build_children(node, scope_env)
        return module_def.instantiate(EvalContext(args=args, children=children, env=scope_env, evaluate=self._instantiate))

    def _build_children(self, node: TreeNode, scope_env: Environment) -> list[ChildInvocation]:
        """Build the child invocations of a module call.

        A ``block`` child is expanded into its statements so that modules
        (e.g. ``children(i)``) see the individual statements rather than the
        wrapping block. Each expanded statement keeps the block's scope.
        """
        children: list[ChildInvocation] = []
        for child in node.children:
            if child.module == "block":
                block_env = scope_env
                if child.variables:
                    block_env = block_env.extend(child.variables)
                children.extend(
                    ChildInvocation(grandchild, block_env) for grandchild in child.children
                )
            else:
                children.append(ChildInvocation(child, scope_env))
        return children
