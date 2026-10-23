from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from manifold_learn.ast.expression import Assignment
    from manifold_learn.ast.invocation import ChildInvocation
    from manifold_learn.ast.module_definition import ModuleDefinition


class Environment:
    """A lexical scope for variable and module name resolution.

    Two parent links exist because OpenSCAD has two scoping rules:

    - Plain names resolve through the lexical chain (``parent``): the scope
      where the name was written.
    - ``$``-prefixed special variables (``$fn``, ``$children``, ...) resolve
      through the dynamic chain (``dynamic_parent``): the scope where the
      current module was *instantiated*.

    Ordinary scopes extend both chains together (``extend``); only module
    bodies (``for_module_body``) split them, binding the lexical chain to the
    definition site and the dynamic chain to the call site.
    """

    def __init__(
        self,
        variables: dict[str, Assignment] | None = None,
        modules: dict[str, ModuleDefinition] | None = None,
        parent: Environment | None = None,
        dynamic_parent: Environment | None = None,
        is_module_scope: bool = False,
    ):
        self._variables = variables if variables is not None else {}
        self._modules = modules if modules is not None else {}
        self._parent = parent
        self._dynamic_parent = dynamic_parent
        self._is_module_scope = is_module_scope

    @classmethod
    def for_module_body(
        cls,
        variables: dict[str, Assignment],
        lexical_parent: Environment,
        dynamic_parent: Environment,
    ) -> Environment:
        """The scope of a module body: variables resolve lexically at the
        definition site, ``$`` variables dynamically at the call site."""
        return cls(
            variables=variables,
            parent=lexical_parent,
            dynamic_parent=dynamic_parent,
            is_module_scope=True,
        )

    def extend(self, variables: dict[str, Assignment] | None = None) -> Environment:
        """A nested scope: its names shadow the parent's; the dynamic chain
        is inherited unchanged (nesting does not cross a module boundary)."""
        return Environment(variables=variables, parent=self, dynamic_parent=self._dynamic_parent)

    def define_variable(self, assignment: Assignment) -> None:
        self._variables[assignment.name] = assignment

    def define_module(self, name: str, definition: ModuleDefinition) -> None:
        self._modules[name] = definition

    def lookup_variable(self, name: str) -> Any:
        env = self
        while env is not None:
            if name in env._variables:
                return env._resolve_binding(name)
            if name.startswith("$") and env._is_module_scope:
                env = env._dynamic_parent
            else:
                env = env._parent
        return None

    def _resolve_binding(self, name: str) -> Any:
        # A definition cannot reference itself: the value is evaluated
        # against this scope with the binding removed, so the right-hand
        # side falls through to the parent scope (OpenSCAD declarative
        # semantics: `{ width = width / 2; }` sees the outer width).
        exclusion = Environment(
            variables={k: v for k, v in self._variables.items() if k != name},
            parent=self._parent,
            dynamic_parent=self._dynamic_parent,
            is_module_scope=self._is_module_scope,
        )
        return self._variables[name].value.evaluate(exclusion)

    def lookup_module(self, name: str) -> ModuleDefinition | None:
        env = self
        while env is not None:
            if name in env._modules:
                return env._modules[name]
            env = env._parent
        return None
