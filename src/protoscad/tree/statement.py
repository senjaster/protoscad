from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from protoscad.diagnostics.spans import SourceSpan

if TYPE_CHECKING:
    from collections.abc import Mapping

    from protoscad.tree.expression import Assignment, Expression

__all__ = [
    "ModuleCallStatement",
    "ModuleDefinitionStatement",
    "SourceSpan",
    "Statement",
    "VariableBindingStatement",
]


@dataclass(kw_only=True)
class Statement:
    """Base class for a statement in a scope.

    A scope is a ``ModuleCallStatement`` whose ``children`` hold the
    statements. The statement's concrete kind discriminates a module call, a
    variable binding, or a module definition.

    ``span`` locates the statement's source text; it is ``None`` for
    synthesized nodes (e.g. the root scope) that have no direct source.
    """

    span: SourceSpan | None = None


@dataclass
class ModuleCallStatement(Statement):
    """An invocation of a module, e.g. ``union() { ... }``.

    ``children`` is the list of statements passed as the module body. A scope
    (the root, a module body, ``let``) is itself a ``ModuleCallStatement``
    whose ``children`` are the scope's statements.
    """

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

    ``body`` is the module body scope: a ``ModuleCallStatement`` whose
    ``children`` are the body's statements.
    """

    name: str
    parameters: Mapping[str, Assignment]
    body: ModuleCallStatement
