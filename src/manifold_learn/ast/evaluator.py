from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from manifold_learn.ast.environment import Environment
from manifold_learn.ast.expression import Assignment
from manifold_learn.ast.manifold import UnionModule, union_geometries
from manifold_learn.ast.module_definition import ModuleDefinition
from manifold_learn.ast.invocation import ChildInvocation, EvalContext
from manifold_learn.ast.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    Statement,
    VariableBindingStatement,
)
from manifold_learn.ast.module_closure import ModuleClosure


class StatementEvaluator:
    """Evaluate a Statement scope.

    OpenSCAD is declarative: a scope is evaluated in three passes regardless
    of source order — register all variable bindings, define all modules, then
    instantiate every module-call statement (implicit union of the results).
    """

    def __init__(self, builtin_modules: Iterable[ModuleDefinition]):
        union = UnionModule()
        self._modules: dict[str, ModuleDefinition] = {m.name: m for m in builtin_modules}
        # "union" is the implicit union backing the top level and module bodies.
        self._modules.setdefault("union", union)

    def evaluate(self, scope: list[Statement]) -> Any:
        env = Environment(modules=self._modules)
        return self._evaluate_scope(scope, env)

    def _evaluate(self, invocation: ChildInvocation) -> Any:
        node = invocation.node
        if isinstance(node, list):
            return self._evaluate_scope(node, invocation.env)
        return self._instantiate(node, invocation.env)

    def _evaluate_scope(self, scope: list[Statement], env: Environment) -> Any:
        """Evaluate a scope declaratively: variables, then modules, then calls."""
        scope_env = self._build_scope_env(scope, env)
        results: list[Any] = []
        for statement in scope:
            if not isinstance(statement, ModuleCallStatement):
                continue
            result = self._instantiate(statement, scope_env)
            if result is None:
                continue
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return union_geometries(results)

    def _build_scope_env(self, scope: list[Statement], env: Environment) -> Environment:
        """Passes 1 and 2: register variable bindings and module definitions."""
        variables: dict[str, Assignment] = {}
        definitions: list[ModuleDefinitionStatement] = []
        for statement in scope:
            if isinstance(statement, VariableBindingStatement):
                variables[statement.name] = Assignment(statement.name, statement.value)
            elif isinstance(statement, ModuleDefinitionStatement):
                definitions.append(statement)

        scope_env = env.extend(variables) if variables else env
        if definitions:
            modules = {
                definition.name: ModuleClosure(
                    definition.name, definition.parameters, definition.body, scope_env
                )
                for definition in definitions
            }
            scope_env = Environment(
                modules=modules,
                parent=scope_env,
                dynamic_parent=scope_env._dynamic_parent,
            )
        return scope_env

    def _instantiate(self, node: ModuleCallStatement, env: Environment) -> Any:
        # `let` is a scope: its children (leading variable bindings plus the
        # body) are evaluated declaratively, mirroring a module body.
        if node.module == "let":
            return self._evaluate_scope(node.children, env)

        # Resolve the module in the caller's scope, not in the scope the call
        # itself introduces for its children.
        module_def = env.lookup_module(node.module)
        if module_def is None:
            raise ValueError(f"Unknown module: {node.module!r}")

        bound = module_def.bind_parameters(node.positional_args, node.named_args)
        args = {name: assignment.value.evaluate(env) for name, assignment in bound.items()}
        body_env = self._build_scope_env(node.children, env)
        children = [
            ChildInvocation(statement, body_env)
            for statement in node.children
            if isinstance(statement, ModuleCallStatement)
        ]
        return module_def.instantiate(
            EvalContext(args=args, children=children, env=body_env, evaluate=self._evaluate)
        )