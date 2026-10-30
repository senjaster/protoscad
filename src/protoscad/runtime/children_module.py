from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any

from protoscad.runtime.module_definition import BuiltinModule, Geometry
from protoscad.tree.expression import Assignment, UndefLiteral

if TYPE_CHECKING:
    from protoscad.runtime.invocation import Invocation
    from protoscad.tree.statement import ModuleCallStatement


class ChildrenModule(BuiltinModule):
    def __init__(self, children: Sequence[ModuleCallStatement]):
        """This is a special pseudo-module that implements
        children(i) syntax for accessing children of user-defined module."""
        BuiltinModule.__init__(self)
        self._children = children

    def instantiate(self, ctx: Invocation) -> Geometry | list[Geometry] | None:
        i = ctx.arg_values["i"]
        # No argument selects every child.
        if i is None:
            return self._select_many(ctx, range(len(self._children)))
        # A vector argument selects the listed children, in order.
        if isinstance(i, list):
            return self._select_many(ctx, i)

        index = self._normalize_index(i)
        if index is None or index < 0 or index >= len(self._children):
            return None
        return ctx.evaluate(self._children[index], ctx.child_env)

    def _select_many(self, ctx: Invocation, indices: Sequence[Any]) -> list[Geometry]:
        results: list[Geometry] = []
        for i in indices:
            index = self._normalize_index(i)
            if index is None or index < 0 or index >= len(self._children):
                continue
            result = ctx.evaluate(self._children[index], ctx.child_env)
            if result is None:
                continue
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
        return results

    @staticmethod
    def _normalize_index(i: Any) -> int | None:
        # The index arrives as a float (NumberLiteral evaluates to float);
        # accept any whole-number value.
        if isinstance(i, float) and i.is_integer():
            return int(i)
        if isinstance(i, int):
            return i
        return None

    @property
    def name(self) -> str:
        return "children"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(optional={"i": UndefLiteral()})
