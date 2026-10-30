from __future__ import annotations

from typing import Any

import pytest
from antlr4 import CommonTokenStream, InputStream

from protoscad.builtins import CubeModule, ResizeModule
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


def test_resize_fits_bounding_box_to_newsize():
    result = evaluate_with_modules(
        "resize(newsize = [30, 60, 10]) cube([1,2,3]);",
        [ResizeModule(), CubeModule()],
    )
    assert result.bounding_box() == pytest.approx((0, 0, 0, 30, 60, 10))


def test_resize_zero_axis_is_left_unchanged():
    # A zero target leaves that axis at its original size.
    result = evaluate_with_modules(
        "resize(newsize = [30, 0, 10]) cube(1);",
        [ResizeModule(), CubeModule()],
    )
    assert result.bounding_box() == pytest.approx((0, 0, 0, 30, 1, 10))


def test_resize_auto_scales_zero_axis_to_match_aspect_ratio():
    # With auto, the zero axis scales so the object keeps its proportions:
    # cube is 1x1x1, so the Y axis also becomes 30 (matching X).
    result = evaluate_with_modules(
        "resize(newsize = [30, 0, 10], auto = true) cube(1);",
        [ResizeModule(), CubeModule()],
    )
    assert result.bounding_box() == pytest.approx((0, 0, 0, 30, 30, 10))


def test_resize_keeps_volume_proportional():
    result = evaluate_with_modules(
        "resize(newsize = [2, 2, 2]) cube(1);",
        [ResizeModule(), CubeModule()],
    )
    assert result.volume() == pytest.approx(8.0)
