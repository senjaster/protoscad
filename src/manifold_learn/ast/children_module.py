from typing import Sequence, Mapping

from manifold_learn.ast.expression import Assignment, NumberLiteral
from manifold_learn.ast.module_definition import BuiltinModule, EvalContext, ChildInvocation, Geometry


class ChildrenModule(BuiltinModule):
    def __init__(self, children: Sequence[ChildInvocation]):
        BuiltinModule.__init__(self)
        self._children = children

    def instantiate(self, ctx: EvalContext) -> Geometry | list[Geometry] | None:
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
        return ctx.evaluate(self._children[i])

    @property
    def name(self) -> str:
        return "children"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=["i"])



