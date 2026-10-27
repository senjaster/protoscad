from __future__ import annotations

import json

from protoscad.diagnostics import Diagnostic, ErrorCode, ProtoSCADError, SourceSpan, render_json, render_text

SOURCE = """\
module Foo(a, b=2) {
    cube([10, 10, 10]);
}
cbe(10);
"""


def test_point_span_is_zero_width():
    assert SourceSpan.point(3, 7) == SourceSpan(3, 7, 3, 7)


def test_error_carries_diagnostic_and_bare_message():
    error = ProtoSCADError("boom", code=ErrorCode.UNKNOWN_MODULE, span=SourceSpan.point(1, 0), notes=("hint",))
    assert str(error) == "boom"
    assert error.diagnostic.code == ErrorCode.UNKNOWN_MODULE
    assert error.diagnostic.message == "boom"
    assert error.diagnostic.span == SourceSpan.point(1, 0)
    assert error.diagnostic.notes == ("hint",)
    assert error.diagnostic.severity == "error"


def test_render_text_points_at_source():
    diagnostic = Diagnostic(
        code=ErrorCode.UNKNOWN_MODULE,
        message="Unknown module: 'cbe'",
        span=SourceSpan(4, 0, 4, 3),
    )
    assert render_text([diagnostic], SOURCE, file="model.scad") == (
        "error[unknown-module]: Unknown module: 'cbe'\n  --> model.scad:4:1\n  |\n4 | cbe(10);\n  | ^^^"
    )


def test_render_text_columns_are_one_based_in_display():
    diagnostic = Diagnostic(
        code=ErrorCode.SYNTAX,
        message="missing ')'",
        span=SourceSpan(2, 4, 2, 5),
    )
    text = render_text([diagnostic], "cube(1\n    x;\n")
    # Column 4 is displayed as 5.
    assert "  --> 2:5" in text
    assert "    ^" in text


def test_render_text_without_file_shows_position_only():
    diagnostic = Diagnostic(code=ErrorCode.UNKNOWN_MODULE, message="nope", span=SourceSpan(1, 0, 1, 1))
    text = render_text([diagnostic], "x;")
    assert "  --> 1:1" in text


def test_render_text_without_span_omits_snippet():
    diagnostic = Diagnostic(code=ErrorCode.UNKNOWN_OPERATOR, message="invariant broken")
    assert render_text([diagnostic], SOURCE) == "error[unknown-operator]: invariant broken"


def test_render_text_multiline_span_renders_first_line():
    diagnostic = Diagnostic(
        code=ErrorCode.CIRCULAR_DEPENDENCY,
        message="cycle",
        span=SourceSpan(1, 7, 3, 1),
    )
    text = render_text([diagnostic], SOURCE, file="m.scad")
    assert "1 | module Foo(a, b=2) {" in text
    # Carets run from the span start to the end of the displayed first line
    # (7 spaces in, 13 carets: the line is 20 characters long).
    assert "  |        ^^^^^^^^^^^^^" in text


def test_render_text_point_past_end_of_line_renders_single_caret():
    # EOF errors point one past the last character.
    diagnostic = Diagnostic(code=ErrorCode.SYNTAX, message="expected ';'", span=SourceSpan.point(1, 6))
    text = render_text([diagnostic], "cube(1")
    assert "1 | cube(1" in text
    assert text.endswith("  |       ^")


def test_render_text_renders_notes_and_multiple_diagnostics():
    diagnostics = [
        Diagnostic(code=ErrorCode.SYNTAX, message="first", span=SourceSpan(1, 0, 1, 1)),
        Diagnostic(code=ErrorCode.SYNTAX, message="second", notes=("try harder",)),
    ]
    text = render_text(diagnostics, "x;\n")
    assert "error[syntax]: first" in text
    assert "error[syntax]: second" in text
    assert "  = note: try harder" in text
    assert "error[syntax]: second\n  = note: try harder" in text


def test_render_json_is_lsp_shaped():
    diagnostic = Diagnostic(
        code=ErrorCode.SYNTAX,
        message="bad token",
        span=SourceSpan(4, 0, 4, 3),
        notes=("try 'cube'",),
    )
    payload = json.loads(render_json([diagnostic], file="model.scad"))
    assert payload == {
        "diagnostics": [
            {
                "severity": "error",
                "code": "syntax",
                "message": "bad token",
                "file": "model.scad",
                # LSP ranges: 0-based line and character.
                "range": {"start": {"line": 3, "character": 0}, "end": {"line": 3, "character": 3}},
                "notes": ["try 'cube'"],
            }
        ]
    }


def test_render_json_without_span_or_file():
    payload = json.loads(render_json([Diagnostic(code=ErrorCode.UNKNOWN_OPERATOR, message="invariant")]))
    entry = payload["diagnostics"][0]
    assert entry["file"] is None
    assert entry["range"] is None
    assert entry["notes"] == []
