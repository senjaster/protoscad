from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from manifold_learn.runtime.resolver import BindingResolver, DeclarativeResolver

if TYPE_CHECKING:
    from manifold_learn.runtime.module_definition import ModuleDefinition
    from manifold_learn.tree.expression import Assignment


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
        self._forcing: list[str] = []

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
            resolver=lexical_parent._resolver,
        )

    def extend_variables(self, variables: dict[str, Assignment] | None = None) -> Environment:
        """A nested scope: its names shadow the parent's; the dynamic chain
        is inherited unchanged (nesting does not cross a module boundary)."""
        return Environment(
            variables=variables, parent=self, dynamic_parent=self._dynamic_parent, resolver=self._resolver
        )

    def extend_modules(self, modules: Mapping[str, ModuleDefinition] | None = None) -> Environment:
        """A nested scope: its names shadow the parent's; the dynamic chain
        is inherited unchanged (nesting does not cross a module boundary)."""
        return Environment(modules=modules, parent=self, dynamic_parent=self._dynamic_parent, resolver=self._resolver)

    @property
    def resolver(self) -> BindingResolver:
        """The binding-resolution policy in force for this scope tree."""
        return self._resolver

    def lookup_variable(self, name: str) -> Any:
        owner = self._scope_defining(name)
        return owner._binding_value(name) if owner is not None else None

    def resolves(self, name: str) -> bool:
        """Whether ``name`` is bound somewhere along the lookup chains —
        a membership check that forces no values."""
        return self._scope_defining(name) is not None

    def _scope_defining(self, name: str) -> Environment | None:
        """The scope along the lookup chain that binds ``name``, or None.

        Follows the lexical chain, switching to the dynamic chain for
        ``$``-prefixed names at module boundaries (see the class
        docstring). The single place that knows how to walk the chain;
        both value lookup and the forcing-stack resumption go through it.
        """
        env: Environment | None = self
        while env is not None:
            if name in env._variables:
                return env
            use_dynamic_env = name.startswith("$") and env._is_module_scope
            env = env._dynamic_parent if use_dynamic_env else env._parent
        return None

    def _binding_value(self, name: str) -> Any:
        """The binding's value, forced on first use and memoized
        (call-by-need).

        The forcing stack implements the scope's letrec rules. Reading the
        binding currently being forced (the innermost stack frame) falls
        through to the enclosing scopes — the ``width = width/2`` shadowing
        idiom. Reading an *outer* frame would have to force it again: an
        unguarded cycle, which raises with its path. A guard that stops the
        descent (e.g. an untaken conditional branch) never reaches this
        case, which is what makes guarded recursion legal.
        """
        if name in self._values:
            return self._values[name]
        if name in self._forcing:
            if self._forcing[-1] == name:
                continuation = self._continuation(name)
                return continuation.lookup_variable(name) if continuation is not None else None
            start = self._forcing.index(name)
            raise ValueError("Circular variable dependency: " + " -> ".join([*self._forcing[start:], name]))
        self._forcing.append(name)
        try:
            value = self._variables[name].value.evaluate(self)
        finally:
            self._forcing.pop()
        self._values[name] = value
        return value

    def _continuation(self, name: str) -> Environment | None:
        """Where a self-reference continues: past this scope, along the
        chain a lookup of ``name`` would have taken."""
        if name.startswith("$") and self._is_module_scope:
            return self._dynamic_parent
        return self._parent

    def lookup_module(self, name: str) -> ModuleDefinition | None:
        env: Environment | None = self
        while env is not None:
            if name in env._modules:
                return env._modules[name]
            env = env._parent
        return None
