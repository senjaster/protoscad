from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

from manifold_learn.tree.expression import Assignment, Expression, Literal
from manifold_learn.tree.statement import VariableBindingStatement

if TYPE_CHECKING:
    from manifold_learn.runtime.environment import Environment


class BindingResolver(Protocol):
    """Strategy for building a scope's variable map from its source
    bindings.

    The result feeds the scope ``Environment``. Eager strategies
    (``OpenScadResolver``) evaluate everything now and return constants;
    the lazy ``DeclarativeResolver`` leaves the expressions in place and
    lets the environment force them on first use (call-by-need with cycle
    detection). Call arguments and module bodies always see the same map
    either way.
    """

    def resolve(self, parent: Environment, bindings: list[VariableBindingStatement]) -> dict[str, Assignment]:
        """Build the variable map for the scope that extends ``parent``."""
        ...


class DeclarativeResolver:
    """Letrec semantics: a scope is a set of simultaneous definitions.

    Bindings are stored unevaluated and forced on first use, so order
    within a scope carries no meaning:

    - Redefinition *replaces* the definition: only the last binding of a
      name exists (``x=1; y=x; x=10`` yields y=10; ``q=zz; q=7`` never
      looks at zz).
    - A name bound in a scope shadows the parent for the whole scope
      (``m=5; union() { y=m; m=1; }`` yields y=1).
    - Self-reference reads the enclosing scope (``width = width/2``).
    - Guarded cycles are legal: a guard that stops the descent (e.g. the
      untaken branch of a conditional) never forces the cycle. An
      unguarded cycle raises with its forcing path (``x -> y -> x``) —
      but only when the value is actually used.
    - Unknown names in bindings are rejected at scope setup, even for
      bindings that are never used.
    """

    def resolve(self, parent: Environment, bindings: list[VariableBindingStatement]) -> dict[str, Assignment]:
        final: dict[str, Assignment] = {}
        for binding in bindings:
            final[binding.name] = Assignment(binding.name, binding.value)
        scope_names = set(final)
        for name, assignment in final.items():
            for ref in assignment.value.referenced_names():
                if ref not in scope_names and not parent.resolves(ref):
                    raise ValueError(f"Unknown variable {ref!r} in the definition of {name!r}")
        return final


class OpenScadResolver:
    """OpenSCAD-faithful semantics, verified empirically against real
    OpenSCAD (see QUIRKS.md).

    - Only the *last* binding of each name is evaluated — an earlier
      shadowed binding never runs, exactly as in OpenSCAD.
    - A binding's right-hand side sees the *final* value of any same-scope
      variable whose *first* definition is at or before the binding's
      position (so ``x=1; y=x; x=10`` yields y=10).
    - A variable first defined *after* the binding resolves in the parent
      scope instead (``m=5; union() { y=m; m=1; }`` yields y=5); if the
      parent has no value either, that is an error.
    - Cyclic final definitions raise (OpenSCAD degrades them to undef with
      warnings; we prefer a loud failure).
    """

    def resolve(self, parent: Environment, bindings: list[VariableBindingStatement]) -> dict[str, Assignment]:
        final_expr, first_pos, final_pos = self._collect(bindings)
        deps = self._dependencies(parent, final_expr, first_pos, final_pos)
        values = self._evaluate(parent, final_expr, deps, self._topological(deps))
        return {name: Assignment(name, Literal(value)) for name, value in values.items()}

    def _collect(
        self, bindings: list[VariableBindingStatement]
    ) -> tuple[dict[str, Expression], dict[str, int], dict[str, int]]:
        final_expr: dict[str, Expression] = {}
        first_pos: dict[str, int] = {}
        final_pos: dict[str, int] = {}
        for pos, statement in enumerate(bindings):
            first_pos.setdefault(statement.name, pos)
            final_pos[statement.name] = pos
            final_expr[statement.name] = statement.value
        return final_expr, first_pos, final_pos

    def _dependencies(
        self,
        parent: Environment,
        final_expr: dict[str, Expression],
        first_pos: dict[str, int],
        final_pos: dict[str, int],
    ) -> dict[str, set[str]]:
        # n reads the final value of every same-scope m that is referenced
        # and whose first definition is at or before n's own (final)
        # binding. Same-name references are excluded so a binding shadows
        # its parent's value on its right-hand side (`width = width / 2`
        # sees the outer width).
        deps: dict[str, set[str]] = {}
        for name, expr in final_expr.items():
            reads: set[str] = set()
            for ref in expr.referenced_names():
                if ref == name:
                    continue
                if ref in first_pos:
                    if first_pos[ref] <= final_pos[name]:
                        reads.add(ref)
                    elif parent.lookup_variable(ref) is None:
                        raise ValueError(
                            f"Variable {ref!r} is used in the definition of {name!r} "
                            "before its first assignment in this scope"
                        )
                elif parent.lookup_variable(ref) is None:
                    raise ValueError(f"Unknown variable {ref!r} in the definition of {name!r}")
            deps[name] = reads
        return deps

    def _topological(self, deps: dict[str, set[str]]) -> list[str]:
        # Depth-first topological order; cycles raise.
        order: list[str] = []
        state: dict[str, int] = {}

        def visit(node: str) -> None:
            mark = state.get(node, 0)
            if mark == 1:
                raise ValueError(f"Circular variable dependency involving {node!r}")
            if mark == 2:
                return
            state[node] = 1
            for dep in sorted(deps[node]):
                visit(dep)
            state[node] = 2
            order.append(node)

        for name in deps:
            visit(name)
        return order

    def _evaluate(
        self,
        parent: Environment,
        final_expr: dict[str, Expression],
        deps: dict[str, set[str]],
        order: list[str],
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}
        for name in order:
            view = {dep: Assignment(dep, Literal(values[dep])) for dep in deps[name]}
            values[name] = final_expr[name].evaluate(parent.extend_variables(view))
        return values
