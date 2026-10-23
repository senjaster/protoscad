from typing import Mapping, Sequence

from manifold3d import Manifold, OpType

from manifold_learn.ast.expression import Assignment, NumberLiteral
from manifold_learn.ast.module_definition import BuiltinModule, EvalContext


def union_geometries(geometries: Sequence[Manifold]) -> Manifold | None:
    """Implicit union: what a scope with several instantiations produces."""
    if not geometries:
        return None
    if len(geometries) == 1:
        return geometries[0]
    return Manifold.batch_boolean(list(geometries), OpType.Add)


class UnionModule(BuiltinModule):
    """Implicit union of all children.

    Backs bare blocks, the top level, and ``let``, as well as the
    user-visible ``union()``.
    """

    def instantiate(self, ctx: EvalContext) -> Manifold | None:
        return union_geometries(ctx.evaluate_children())

    @property
    def name(self) -> str:
        return "union"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}


class CubeModule(BuiltinModule):
    def instantiate(self, ctx: EvalContext) -> Manifold:
        size = ctx.args["size"]
        if not isinstance(size, list):
            size = [size, size, size]
        center = bool(ctx.args["center"])
        return Manifold.cube(size, center)

    @property
    def name(self) -> str:
        return "cube"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(
            required=("size",),
            optional={"center": NumberLiteral(0)},
        )


class TranslateModule(BuiltinModule):
    def instantiate(self, ctx: EvalContext) -> Manifold | None:
        child = union_geometries(ctx.evaluate_children())
        if child is None:
            return None
        return child.translate(ctx.args["offset"])

    @property
    def name(self) -> str:
        return "translate"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("offset",))
