from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from manifold_learn.ast.environment import Environment
from manifold_learn.ast.expression import Assignment
from manifold_learn.ast.invocation import ChildInvocation, EvalContext
from manifold_learn.ast.manifold import LetModule, UnionModule
from manifold_learn.ast.module_closure import ModuleClosure
from manifold_learn.ast.module_definition import ModuleDefinition
from manifold_learn.ast.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    VariableBindingStatement,
)


class StatementEvaluator:
    """Evaluate a Statement scope.

    OpenSCAD is declarative: a scope is evaluated in three passes regardless
    of source order — register all variable bindings, define all modules, then
    instantiate every module-call statement (implicit union of the results).
    """

    def __init__(self, builtin_modules: Iterable[ModuleDefinition]):
        union = UnionModule()
        self._modules: dict[str, ModuleDefinition] = {m.name: m for m in builtin_modules}
        # "union" and "let" are scopes: the implicit union backing the top
        # level and module bodies, and the let scoping construct.
        self._modules.setdefault("union", union)
        self._modules.setdefault("let", LetModule())

    def evaluate(self, root: ModuleCallStatement) -> Any:
        """"""
        env = Environment(modules=self._modules)
        return self._evaluate_statement(root, env)

    def _build_children_env(self, node: ModuleCallStatement, env: Environment) -> Environment:
        """
        Build an environment for a node's children.
        :param node: the node whose children are being evaluated
        :param env: parent environment
        :return: extended environment with the scope's variables and modules
        """

        # Pass 1 - bind variables (and also stash module definitions for pass 2)
        variables: dict[str, Assignment] = {}
        definitions: list[ModuleDefinitionStatement] = []
        for statement in node.children:
            if isinstance(statement, VariableBindingStatement):
                variables[statement.name] = Assignment(statement.name, statement.value)
            elif isinstance(statement, ModuleDefinitionStatement):
                definitions.append(statement)

        # Pass 2 - build closures taking the scope's variables into account
        scope_env = env.extend_variables(variables) if variables else env
        if definitions:
            modules = {
                definition.name: ModuleClosure.from_definition(
                    definition,
                    scope_env,
                )
                for definition in definitions
            }
            scope_env = scope_env.extend_modules(modules)
        return scope_env

    def _evaluate_statement(self, node: ModuleCallStatement, env: Environment) -> Any:
        # Resolve the module in the caller's scope, not in the scope the call
        # itself introduces for its children.
        module_def = env.lookup_module(node.module)
        if module_def is None:
            raise ValueError(f"Unknown module: {node.module!r}")

        children_env = self._build_children_env(node, env)

        bound = module_def.bind_parameters(node.positional_args, node.named_args)
        args = {name: assignment.value.evaluate(env) for name, assignment in bound.items()}
        children = [
            ChildInvocation(statement, children_env)
            for statement in node.children
            if isinstance(statement, ModuleCallStatement)
        ]
        return module_def.instantiate(
            EvalContext(
                args=args,
                children=children,
                env=children_env,
                evaluate=self._evaluate_statement,
            )
        )
