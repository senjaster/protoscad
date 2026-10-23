from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

    from manifold_learn.ast.expression import Assignment, Expression


class Statement(ABC):
    """Base class for a statement in a scope.

    A scope is a plain ``list[Statement]``. The statement's concrete kind
    discriminates a module call, a variable binding, or a module definition.
    """


@dataclass
class ModuleCallStatement(Statement):
    """An invocation of a module, e.g. ``union() { ... }``.

    ``children`` is the list of statements passed as the module body."""

    module: str
    positional_args: list[Expression] = field(default_factory=list)
    named_args: dict[str, Expression] = field(default_factory=dict)
    children: list[Statement] = field(default_factory=list)


@dataclass
class VariableBindingStatement(Statement):
    """A variable binding, e.g. ``x = 10;``."""

    name: str
    value: Expression


@dataclass
class ModuleDefinitionStatement(Statement):
    """A user-defined module, e.g. ``module Foo(a, b=2) { ... }``.

    ``body`` is the module body scope: a list of statements.
    """

    name: str
    parameters: Mapping[str, Assignment]
    body: list[Statement] = field(default_factory=list)