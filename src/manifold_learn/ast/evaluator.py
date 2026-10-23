from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from manifold_learn.ast.environment import Environment
from manifold_learn.ast.manifold import UnionModule
from manifold_learn.ast.module_definition import ChildInvocation, EvalContext, ModuleDefinition
from manifold_learn.ast.tree_node import TreeNode


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
        if node.variables:
            env = env.extend(node.variables)

        module_def = env.lookup_module(node.module)
        if module_def is None:
            raise ValueError(f"Unknown module: {node.module!r}")

        bound = module_def.bind_parameters(node.positional_args, node.named_args)
        args = {name: assignment.value.evaluate(env) for name, assignment in bound.items()}
        children = [ChildInvocation(child, env) for child in node.children]
        return module_def.instantiate(EvalContext(args=args, children=children, env=env, evaluate=self._instantiate))
