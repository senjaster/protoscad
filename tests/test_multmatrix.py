from __future__ import annotations

from typing import Any

import pytest
from antlr4 import CommonTokenStream, InputStream

from protoscad.builtins import CubeModule, MultmatrixModule
from protoscad.grammar.OpenSCADLexer import OpenSCADLexer
from protoscad.grammar.OpenSCADParser import OpenSCADParser
from protoscad.runtime.evaluator import evaluate
from protoscad.tree.statement import ModuleCallStatement
from protoscad.tree.visitor import AstOpenSCADVisitor


def parse_scad(source: str) -> ModuleCallStatement:
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


def evaluate_with_modules(source: str, modules) -> Any:
    return evaluate(parse_scad(source), list(modules))


def test_multmatrix_translates():
    result = evaluate_with_modules(
        "multmatrix(m = [[1, 0, 0, 10], [0, 1, 0, 20], [0, 0, 1, 30], [0, 0, 0, 1]]) cube(1);",
        [MultmatrixModule(), CubeModule()],
    )
    assert result.bounding_box() == pytest.approx((10, 20, 30, 11, 21, 31))


def test_multmatrix_scales():
    result = evaluate_with_modules(
        "multmatrix(m = [[2, 0, 0, 0], [0, 3, 0, 0], [0, 0, 4, 0], [0, 0, 0, 1]]) cube(1);",
        [MultmatrixModule(), CubeModule()],
    )
    assert result.bounding_box() == pytest.approx((0, 0, 0, 2, 3, 4))


def test_multmatrix_shears():
    # Shear X by Y: x' = x + 2y, so the (0,1,0) corner maps to (2,1,0).
    result = evaluate_with_modules(
        "multmatrix(m = [[1, 2, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) cube(1);",
        [MultmatrixModule(), CubeModule()],
    )
    assert result.bounding_box() == pytest.approx((0, 0, 0, 3, 1, 1))


def test_multmatrix_chains_with_other_transforms():
    result = evaluate_with_modules(
        "multmatrix(m = [[1, 0, 0, 5], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) cube(1);",
        [MultmatrixModule(), CubeModule()],
    )
    assert result.volume() == pytest.approx(1.0)
    assert result.bounding_box() == pytest.approx((5, 0, 0, 6, 1, 1))
