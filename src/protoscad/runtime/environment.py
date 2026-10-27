from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.runtime.resolver import BindingResolver, DeclarativeResolver

if TYPE_CHECKING:
    from protoscad.runtime.module_definition import ModuleDefinition
    from protoscad.tree.expression import Assignment


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

    Variable bindings are letrec-shaped and lazy: a definition is forced on
    first read and memoized (``_binding_value``). All names bound in a scope
    are therefore visible to each other regardless of source order — an
    unguarded cycle raises, a guarded one (a condition that stops the
    descent) resolves.
    """

    def __init__(
        self,
        variables: Mapping[str, Assignment] | None = None,
        modules: Mapping[str, ModuleDefinition] | None = None,
        parent: Environment | None = None,
        dynamic_parent: Environment | None = None,
        is_module_scope: bool = False,
        resolver: BindingResolver | None = None,
    ):
        self._variables = variables if variables is not None else {}
        self._modules = modules if modules is not None else {}
        self._parent = parent
        self._dynamic_parent = dynamic_parent
        self._is_module_scope = is_module_scope
        self._resolver = resolver if resolver is not None else DeclarativeResolver()
        self._values: dict[str, Any] = {}
        self._forcing_stack: list[str] = []  # Variable evaluation stack

    @classmethod
    def for_module_body(
        cls,
        variables: dict[str, Assignment],
        lexical_parent: Environment,
        dynamic_parent: Environment,
    ) -> Environment:
        """
        Create a module body scope:

        Lexical parent is where the module was defined.
        Dynamic parent is where the module was called.
        """
        return cls(
            variables=variables,
            parent=lexical_parent,
            dynamic_parent=dynamic_parent,
            is_module_scope=True,
            resolver=lexical_parent._resolver,
        )

    def extend_variables(self, variables: dict[str, Assignment] | None = None) -> Environment:
        """
        Creates a new nested scope with additional variables defined
        """
        return Environment(
            variables=variables, parent=self, dynamic_parent=self._dynamic_parent, resolver=self._resolver
        )

    def extend_modules(self, modules: Mapping[str, ModuleDefinition] | None = None) -> Environment:
        """Creates a new nested scope with additional modules defined"""
        return Environment(modules=modules, parent=self, dynamic_parent=self._dynamic_parent, resolver=self._resolver)

    @property
    def resolver(self) -> BindingResolver:
        """The binding-resolution policy in force for this scope tree."""
        return self._resolver

    def lookup_variable(self, name: str) -> Any:
        """Return a variable's value, forcing it if necessary."""
        return self._resolve(name, start=self)

    def resolves(self, name: str) -> bool:
        """Whether ``name`` is bound somewhere along the lookup chains —
        a membership check that forces no values."""
        return self._find_defining_scope(name) is not None

    def _find_defining_scope(self, name: str) -> Environment | None:
        """Pure membership walk — no forcing, no side effects."""
        env: Environment | None = self
        while env is not None:
            if name in env._variables:
                return env
            env = env._next_scope(name)
        return None

    def _next_scope(self, name: str) -> Environment | None:
        """The scope the chain-walk moves to next when looking for ``name``:
        the dynamic parent for a ``$name`` crossing a module boundary,
        the lexical parent otherwise."""
        use_dynamic = name.startswith("$") and self._is_module_scope
        return self._dynamic_parent if use_dynamic else self._parent

    def _resolve(self, name: str, start: Environment | None) -> Any:
        """Walk the chain for ``name`` starting at ``start`` and force the
        binding where it's found."""
        env = start
        while env is not None:
            if name in env._variables:
                return env._force(name)
            env = env._next_scope(name)
        return None

    def _force(self, name: str) -> Any:
        """Compute (once) the value bound to ``name`` in *this* scope.
        Letrec-with-shadowing: re-entering the binding currently on top of
        the forcing stack resumes the walk one scope further along the
        chain (the ``width = width/2`` idiom); re-entering an outer,
        still-forcing binding is an unguarded cycle.
        """
        if name in self._values:
            # Already computed
            return self._values[name]

        if name in self._forcing_stack:
            # There might be a circular variable dependency
            if self._forcing_stack[-1] == name:
                # False positive - resolve the same name in the parent scope
                return self._resolve(name, start=self._next_scope(name))
            # A real circular dependency. Find where it begins:
            start = self._forcing_stack.index(name)
            raise ProtoSCADError(
                "Circular variable dependency: " + " -> ".join([*self._forcing_stack[start:], name]),
                code=ErrorCode.CIRCULAR_DEPENDENCY,
                span=self._variables[name].value.span,
            )

        # Not forced yet - force it now
        self._forcing_stack.append(name)
        try:
            value = self._variables[name].value.evaluate(self)
        finally:
            self._forcing_stack.pop()
        self._values[name] = value
        return value

    def lookup_module(self, name: str) -> ModuleDefinition | None:
        env: Environment | None = self
        while env is not None:
            if name in env._modules:
                return env._modules[name]
            env = env._parent
        return None
