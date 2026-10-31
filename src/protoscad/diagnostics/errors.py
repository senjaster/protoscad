from __future__ import annotations

from collections.abc import Sequence

from protoscad.diagnostics.diagnostic import Diagnostic, ErrorCode
from protoscad.diagnostics.spans import SourceSpan


class ProtoSCADError(Exception):
    """A ProtoSCAD failure carrying a structured ``Diagnostic``.

    One exception class for every user-facing failure — syntax, name
    resolution, evaluation; the diagnostic's ``code`` discriminates.
    ``str(error)`` is the bare message so tracebacks stay readable: the
    located, formatted output comes from the renderers in
    ``protoscad.diagnostics.render``.
    """

    def __init__(
        self,
        message: str,
        *,
        code: ErrorCode,
        span: SourceSpan | None = None,
        notes: Sequence[str] = (),
    ) -> None:
        self.diagnostic = Diagnostic(code=code, message=message, span=span, notes=tuple(notes))
        super().__init__(message)


class GeometryError(Exception):
    """A geometry-pipeline failure that has no location of its own.

    Raised by builtin helpers (``builtins._operations``) — code that knows
    *what* went wrong but not *where*: it works on already-evaluated
    geometry, and the source location of the responsible call belongs to
    the evaluator's world. ``Invocation`` catches it at the module call
    being instantiated — the innermost call whose body raised — and
    re-raises it as a located ``ProtoSCADError`` with code ``type-error``.
    """
