from __future__ import annotations

import pytest

from protoscad.diagnostics import ErrorCode, ProtoSCADError, SourceSpan
from protoscad.parser import parse_scad


def test_missing_closing_paren_raises_syntax_error_with_token_span():
    with pytest.raises(ProtoSCADError) as excinfo:
        parse_scad("cube(1;\n")
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.SYNTAX
    # The offending ';' on line 1, column 6.
    assert diagnostic.span == SourceSpan(1, 6, 1, 7)


def test_illegal_character_raises_with_point_span():
    with pytest.raises(ProtoSCADError) as excinfo:
        parse_scad("cube(1);\n@\n")
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.SYNTAX
    # Lexer errors carry no token: a zero-width span at the '@'.
    assert diagnostic.span == SourceSpan.point(2, 0)


def test_unterminated_call_at_eof_raises():
    with pytest.raises(ProtoSCADError) as excinfo:
        parse_scad("cube(1")
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.SYNTAX
    assert diagnostic.span is not None
    assert diagnostic.span.start_line == 1


def test_valid_source_parses_without_listener_output(capsys):
    scope = parse_scad("cube([1, 2, 3]);\n")
    assert scope.module == "union"
    # ANTLR's default stderr reporting is disabled: nothing is printed even
    # on success paths that previously exercised recovery.
    assert capsys.readouterr().err == ""
