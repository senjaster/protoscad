from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from protoscad.builtins import LetModule, UnionModule
from protoscad.runtime.environment import Environment
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import ModuleDefinition
from protoscad.runtime.resolver import BindingResolver
from protoscad.tree.statement import ModuleCallStatement


def evaluate(
    root: ModuleCallStatement,
    builtin_modules: Iterable[ModuleDefinition],
    resolver: BindingResolver | None = None,
) -> Any:
    """Evaluate the root scope produced by the visitor.

    The root scope's module table is the registry the caller supplies,
    plus the two scope constructs: ``union`` backs bare blocks and the
    implicit top-level union, ``let`` is the scoping construct. Everything
    else — dispatch, scopes, recursion — lives on ``Invocation``.

    ``resolver`` selects the scope-binding policy (``DeclarativeResolver``'s
    lazy letrec by default; ``OpenScadResolver`` reproduces OpenSCAD's
    quirks).
    """
    modules: dict[str, ModuleDefinition] = {str(m.name): m for m in builtin_modules}
    modules.setdefault("union", UnionModule())
    modules.setdefault("let", LetModule())
    return Invocation.evaluate(root, Environment(modules=modules, resolver=resolver))
