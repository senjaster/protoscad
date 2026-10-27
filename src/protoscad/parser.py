from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from protoscad.diagnostics import ErrorCode, ProtoSCADError, SourceSpan
from protoscad.grammar.OpenSCADLexer import OpenSCADLexer
from protoscad.grammar.OpenSCADParser import OpenSCADParser
from protoscad.tree import AstOpenSCADVisitor
from protoscad.tree.statement import ModuleCallStatement


class _FailFastErrorListener(ErrorListener):
    """Turn the first lexical or syntax error into a raised
    ``ProtoSCADError``.

    ANTLR's default listener prints to stderr and lets parsing continue on a
    broken tree; we fail loudly instead. Raising a non-``RecognitionException``
    from the listener slips past the generated rules' recovery handlers and
    aborts the parse.
    """

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e) -> None:
        if offendingSymbol is not None:
            span = SourceSpan(
                start_line=line,
                start_column=column,
                end_line=offendingSymbol.line,
                end_column=offendingSymbol.column + len(offendingSymbol.text or ""),
            )
        else:
            # Lexer errors carry no token; point at the exact position.
            span = SourceSpan.point(line, column)
        raise ProtoSCADError(msg, code=ErrorCode.SYNTAX, span=span) from None


def parse_scad(source: str) -> ModuleCallStatement:
    """Parse source via the OpenSCAD grammar, returning the root scope call.

    Raises ``ProtoSCADError`` (code ``syntax``) on the first lexical or
    syntax error instead of ANTLR's recover-and-continue behavior.
    """
    lexer = OpenSCADLexer(InputStream(source))
    lexer.removeErrorListeners()
    lexer.addErrorListener(_FailFastErrorListener())
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(_FailFastErrorListener())
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)
