from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from protoscad.diagnostics.spans import SourceSpan


class Severity(StrEnum):
    """How loud a diagnostic is. Warnings are reserved for future
    OpenSCAD-style non-fatal reports; everything currently raised is an
    error."""

    ERROR = "error"
    WARNING = "warning"


class ErrorCode(StrEnum):
    """Stable machine-readable identifier of a failure kind.

    Codes key IDE-side filtering and documentation. The human message is
    free to change; a code is not.
    """

    SYNTAX = "syntax"
    UNKNOWN_MODULE = "unknown-module"
    UNKNOWN_PARAMETER = "unknown-parameter"
    TOO_MANY_POSITIONAL_ARGS = "too-many-positional-args"
    MISSING_REQUIRED_PARAMETER = "missing-required-parameter"
    UNKNOWN_VARIABLE = "unknown-variable"
    USE_BEFORE_ASSIGNMENT = "use-before-assignment"
    CIRCULAR_DEPENDENCY = "circular-dependency"
    UNKNOWN_OPERATOR = "unknown-operator"
    TYPE_ERROR = "type-error"
    INVALID_INDEX = "invalid-index"
    INDEX_OUT_OF_RANGE = "index-out-of-range"
    UNKNOWN_FUNCTION = "unknown-function"
    INVALID_ARGUMENT = "invalid-argument"
    ASSERTION_FAILED = "assertion-failed"


@dataclass(frozen=True)
class Diagnostic:
    """One reported problem, in a format-neutral structured form.

    Raise sites build this once; renderers turn it into plaintext (with a
    source snippet) or JSON (LSP-shaped ranges) — neither is involved when
    the error is created. ``file`` is deliberately absent: errors are raised
    deep in evaluation where no filename is known, so the reporting boundary
    (the CLI) attaches it when rendering.
    """

    code: ErrorCode
    message: str
    span: SourceSpan | None = None
    severity: Severity = Severity.ERROR
    notes: tuple[str, ...] = ()
