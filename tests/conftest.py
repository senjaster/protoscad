from __future__ import annotations

import pytest
from antlr4 import CommonTokenStream, InputStream

from manifold_learn.ast.tree_node import TreeNode
from manifold_learn.ast_visitor import AstOpenSCADVisitor
from manifold_learn.grammar.OpenSCADLexer import OpenSCADLexer
from manifold_learn.grammar.OpenSCADParser import OpenSCADParser


def parse_scad(source: str) -> TreeNode:
    """Parse OpenSCAD source text and build the AST via the visitor."""
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


@pytest.fixture
def visitor() -> AstOpenSCADVisitor:
    return AstOpenSCADVisitor()