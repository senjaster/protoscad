from __future__ import annotations

import json
from collections.abc import Sequence

from protoscad.diagnostics.diagnostic import Diagnostic
from protoscad.diagnostics.spans import SourceSpan


def render_text(diagnostics: Sequence[Diagnostic], source: str, file: str | None = None) -> str:
    """Format diagnostics as human-readable text with source snippets,
    rustc-style:

        error[unknown-module]: Unknown module: 'cbe'
          --> model.scad:3:5
           |
         3 |     cbe(10);
           |     ^^^

    ``source`` is the text the diagnostics refer to; it provides the quoted
    lines. Lines are displayed 1-based and columns as 1-based (a
    ``SourceSpan`` column is 0-based).
    """
    lines = source.splitlines()
    return "\n\n".join(_render_one(diagnostic, lines, file) for diagnostic in diagnostics)


def render_json(diagnostics: Sequence[Diagnostic], file: str | None = None) -> str:
    """Format diagnostics as JSON for tooling (IDE highlighting).

    ``range`` follows the Language Server Protocol: 0-based line and
    character offsets, ``end`` exclusive.
    """
    payload = {"diagnostics": [_json_one(diagnostic, file) for diagnostic in diagnostics]}
    return json.dumps(payload, indent=2)


def _render_one(diagnostic: Diagnostic, lines: list[str], file: str | None) -> str:
    out = [f"{diagnostic.severity}[{diagnostic.code}]: {diagnostic.message}"]
    if diagnostic.span is not None:
        location = f"{diagnostic.span.start_line}:{diagnostic.span.start_column + 1}"
        out.append(f"  --> {file}:{location}" if file is not None else f"  --> {location}")
        out.extend(_snippet(diagnostic.span, lines))
    out.extend(f"  = note: {note}" for note in diagnostic.notes)
    return "\n".join(out)


def _snippet(span: SourceSpan, lines: list[str]) -> list[str]:
    # A point one past the last character (EOF errors) renders as a single
    # caret right after the line; a span crossing lines renders its first
    # line with carets to end of line.
    text = lines[span.start_line - 1] if 0 < span.start_line <= len(lines) else ""
    gutter = " " * len(str(span.start_line))
    start = min(span.start_column, len(text))
    length = max(span.end_column - start, 1) if span.end_line == span.start_line else max(len(text) - start, 1)
    return [
        f"{gutter} |",
        f"{span.start_line} | {text}",
        f"{gutter} | {' ' * start}{'^' * length}",
    ]


def _json_one(diagnostic: Diagnostic, file: str | None) -> dict[str, object]:
    range_: dict[str, object] | None = None
    if diagnostic.span is not None:
        range_ = {
            "start": {"line": diagnostic.span.start_line - 1, "character": diagnostic.span.start_column},
            "end": {"line": diagnostic.span.end_line - 1, "character": diagnostic.span.end_column},
        }
    return {
        "severity": str(diagnostic.severity),
        "code": str(diagnostic.code),
        "message": diagnostic.message,
        "file": file,
        "range": range_,
        "notes": list(diagnostic.notes),
    }
