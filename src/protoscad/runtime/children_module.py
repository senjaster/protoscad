from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from protoscad.runtime.module_definition import BuiltinModule, Geometry
from protoscad.tree.expression import Assignment

if TYPE_CHECKING:
    from protoscad.runtime.invocation import Invocation
    from protoscad.tree.statement import ModuleCallStatement


class ChildrenModule(BuiltinModule):
    def __init__(self, children: Sequence[ModuleCallStatement]):
        BuiltinModule.__init__(self)
        self._children = children

    def instantiate(self, ctx: Invocation) -> Geometry | list[Geometry] | None:
        i = ctx.args["i"]
        # The index arrives as a float (NumberLiteral evaluates to float);
        # accept any whole-number value.
        if isinstance(i, float) and i.is_integer():
            i = int(i)
        if not isinstance(i, int):
            return None
        if i < 0:
            return None
        if i >= len(self._children):
            return None
        return ctx.evaluate(self._children[i], ctx.child_env)

    @property
    def name(self) -> str:
        return "children"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=["i"])
