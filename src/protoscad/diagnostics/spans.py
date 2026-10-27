from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceSpan:
    """A half-open region of the source text, in 1-based line / 0-based column.

    ``start`` is the first character of the construct, ``end`` the character
    just past its last one. A statement's span lets an error message point at
    the exact source text it came from.

    This is the position vocabulary of the whole error-reporting pipeline:
    diagnostics carry spans, renderers display them (the plaintext renderer
    shows the column as 1-based; the JSON renderer keeps it 0-based,
    LSP-style).
    """

    start_line: int
    start_column: int
    end_line: int
    end_column: int

    @classmethod
    def point(cls, line: int, column: int) -> SourceSpan:
        """A zero-width span at one position (e.g. a lexer error)."""
        return cls(line, column, line, column)
