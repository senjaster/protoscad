from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from manifold_learn.tree.expression import Assignment, Undefined

if TYPE_CHECKING:
    from manifold_learn.runtime.invocation import EvalContext
    from manifold_learn.tree.expression import Expression

Geometry = TypeVar("Geometry")


@dataclass(frozen=True)
class ParameterBindings:
    """Bound module parameters, unevaluated, split by the scope in which
    each expression must resolve.

    - ``explicit``: arguments supplied at the call site — they resolve in
      the caller's scope.
    - ``defaults``: parameters the caller did not supply — their default
      expressions resolve at the module's definition site (the same lexical
      scope as the body; this is what makes ``use``-style library defaults
      work).
    """

    explicit: Mapping[str, Assignment]
    defaults: Mapping[str, Assignment]


class ModuleDefinition[Geometry](ABC):
    """A module that can be invoked to produce geometry.

    Two concrete kinds exist:

    - ``BuiltinModule``: registered at the top-level scope for the
      primitives and operations shipped with the language (e.g. ``cube``,
      ``cylinder``, ``difference``).
    - ``UserDefinedModule``: defined in source via ``module Name(...) { ... }``
      and carrying its own AST subtree.

    Both share a name, the formal parameters as assignments (an ``Undefined``
    value marks a required parameter with no default), and an ``instantiate``
    method that produces geometry, deciding for itself which children to
    evaluate.
    """

    @abstractmethod
    def instantiate(self, ctx: EvalContext) -> Geometry | list[Geometry] | None:
        """Instantiate this module. May return a single geometry, several
        (e.g. a loop unrolling its body), or none."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def parameters(self) -> Mapping[str, Assignment]:
        raise NotImplementedError

    def bind_parameters(
        self, positional_args: list[Expression], named_args: dict[str, Expression]
    ) -> ParameterBindings:
        """Bind the given arguments to the parameters of this module.

        ``$``-prefixed named arguments must be diverted to the special-
        variable overlay by the caller before binding; they are not
        parameters, so passing one through is an unknown-parameter error.

        The arguments are bound in the following order:
        1. Positional arguments
        2. Named arguments
        3. Default values
        """
        parameters = self.parameters
        explicit: dict[str, Assignment] = {}

        if len(positional_args) > len(parameters):
            raise ValueError(
                f"Module {self.name!r} takes at most {len(parameters)} positional arguments, got {len(positional_args)}"
            )
        # Positional arguments bind to the formal parameters in declaration order.
        # Fewer positionals than parameters is legal partial binding; the
        # length check above already rejected the opposite.
        for name, arg in zip(parameters.keys(), positional_args, strict=False):
            explicit[name] = Assignment(name, arg)

        # Named arguments bind by name and take precedence over positional.
        for name, arg in named_args.items():
            if name not in parameters:
                raise ValueError(f"Unknown parameter {name!r} for module {self.name!r}")
            explicit[name] = Assignment(name, arg)

        # Any parameter not bound above keeps its default value.
        defaults = {name: assignment for name, assignment in parameters.items() if name not in explicit}
        return ParameterBindings(explicit=explicit, defaults=defaults)


class BuiltinModule[Geometry](ModuleDefinition, ABC):
    """Base class for the modules shipped with the language.

    A built-in module's parameters are always either required (no default)
    or a fixed literal default. This class provides helpers so subclasses can
    declare them without hand-constructing ``Assignment`` objects.
    """

    @staticmethod
    def required(name: str) -> Assignment:
        """A required parameter with no default value."""
        return Assignment(name, Undefined())

    @staticmethod
    def optional(name: str, default: Expression) -> Assignment:
        """A parameter with a fixed literal default."""
        return Assignment(name, default)

    @staticmethod
    def make_parameters(
        required: Sequence[str] = (),
        optional: Mapping[str, Expression] | None = None,
    ) -> Mapping[str, Assignment]:
        """Build a parameters mapping from required and optional specs.

        ``required`` lists the parameter names that must be supplied by the
        caller; ``optional`` maps each parameter name to its fixed literal
        default.
        """
        built: dict[str, Assignment] = {name: BuiltinModule.required(name) for name in required}
        for name, default in (optional or {}).items():
            built[name] = BuiltinModule.optional(name, default)
        return built
