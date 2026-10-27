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
