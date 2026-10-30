from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest
from antlr4 import CommonTokenStream, InputStream
from manifold3d import Manifold

from protoscad.builtins.assertion import AssertModule
from protoscad.builtins.cube import CubeModule
from protoscad.builtins.echo import EchoModule
from protoscad.builtins.translate import TranslateModule
from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.grammar.OpenSCADLexer import OpenSCADLexer
from protoscad.grammar.OpenSCADParser import OpenSCADParser
from protoscad.runtime.evaluator import evaluate
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.tree.expression import Assignment
from protoscad.tree.statement import ModuleCallStatement
from protoscad.tree.visitor import AstOpenSCADVisitor

MARKER_GEOMETRY = Manifold.cube([1.0, 1.0, 1.0])


def parse_scad(source: str) -> ModuleCallStatement:
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


def evaluate_with_modules(source: str, modules) -> Any:
    return evaluate(parse_scad(source), list(modules))


class ProbeModule(BuiltinModule):
    """Records the evaluated ``value`` argument of each call."""

    def __init__(self):
        self.values: list[Any] = []

    def instantiate(self, ctx: Invocation) -> Manifold:
        self.values.append(ctx.arg_values["value"])
        return MARKER_GEOMETRY

    @property
    def name(self) -> str:
        return "probe"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("value",))


MODULES = (EchoModule(), AssertModule(), ProbeModule())


## =========================================================================
#  echo as a module


def test_echo_module_prints_positional_arguments(capsys):
    evaluate_with_modules('echo("text", 5, [1, true, undef], [0:2:6]);', MODULES)
    assert capsys.readouterr().out == 'ECHO: "text", 5, [1, true, undef], [0:2:6]\n'


def test_echo_module_prints_named_arguments_as_bindings(capsys):
    evaluate_with_modules('echo(width = 5, label = "hi");', MODULES)
    assert capsys.readouterr().out == 'ECHO: width = 5, label = "hi"\n'


def test_echo_module_evaluates_arguments_in_the_calling_scope(capsys):
    evaluate_with_modules("depth = 4; echo(depth, depth + 1);", MODULES)
    assert capsys.readouterr().out == "ECHO: 4, 5\n"


def test_echo_module_produces_no_geometry():
    assert evaluate_with_modules("echo(1);", MODULES) is None


def test_echo_module_passes_chained_children_through():
    result = evaluate_with_modules(
        'echo("wrapping") translate([2, 0, 0]) cube(2);',
        (EchoModule(), CubeModule(), TranslateModule()),
    )
    assert result.volume() == pytest.approx(8.0)


def test_echo_module_passes_blocked_children_through(capsys):
    result = evaluate_with_modules('echo("wrap") { cube(2); }', (EchoModule(), CubeModule()))
    assert result.volume() == pytest.approx(8.0)
    assert capsys.readouterr().out == 'ECHO: "wrap"\n'


def test_echo_without_arguments_prints_an_empty_line(capsys):
    evaluate_with_modules("echo();", MODULES)
    assert capsys.readouterr().out == "ECHO: \n"


## =========================================================================
#  assert as a module


def test_assert_module_passes_when_condition_holds():
    assert evaluate_with_modules('assert(1 < 2, "fine");', MODULES) is None


@pytest.mark.parametrize(
    ("condition", "holds"),
    [
        ("1", True),
        ("-0.0", False),
        ('"text"', True),
        ('""', False),
        ("[1]", True),
        ("[]", False),
        ("true", True),
        ("false", False),
        ("undef", False),
    ],
)
def test_assert_module_condition_openscad_truthiness(condition, holds):
    if holds:
        evaluate_with_modules(f"assert({condition});", MODULES)
    else:
        with pytest.raises(ProtoSCADError, match="Assertion failed"):
            evaluate_with_modules(f"assert({condition});", MODULES)


def test_assert_module_failure_names_the_message():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_with_modules('x = 3; assert(x > 5, "x must exceed 5");', MODULES)
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.message == 'Assertion failed: "x must exceed 5"'
    assert diagnostic.code == ErrorCode.ASSERTION_FAILED


def test_assert_module_failure_without_message():
    with pytest.raises(ProtoSCADError, match="^Assertion failed$"):
        evaluate_with_modules("assert(false);", MODULES)


def test_assert_module_message_is_formatted_like_echo():
    with pytest.raises(ProtoSCADError, match=r"Assertion failed: \[1, true\]"):
        evaluate_with_modules("assert(false, [1, true]);", MODULES)


def test_assert_module_failure_span_points_at_the_call():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_with_modules("assert(false);", MODULES)
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.span is not None
    assert diagnostic.span.start_column == 0


def test_assert_module_named_condition_and_message():
    with pytest.raises(ProtoSCADError, match='Assertion failed: "custom"'):
        evaluate_with_modules('assert(condition = false, message = "custom");', MODULES)


def test_assert_module_missing_condition_raises():
    with pytest.raises(ProtoSCADError, match="Missing required parameter 'condition'"):
        evaluate_with_modules('assert(message = "m");', MODULES)


def test_assert_module_unknown_parameter_raises():
    with pytest.raises(ProtoSCADError, match="Unknown parameter 'bogus'"):
        evaluate_with_modules("assert(1, bogus = 2);", MODULES)


def test_assert_module_too_many_positional_arguments_raise():
    with pytest.raises(ProtoSCADError, match="at most 2 positional"):
        evaluate_with_modules("assert(1, 2, 3);", MODULES)


def test_assert_module_passes_children_through_when_condition_holds():
    result = evaluate_with_modules(
        'assert(1 < 2, "guard") translate([2, 0, 0]) cube(2);',
        (AssertModule(), CubeModule(), TranslateModule()),
    )
    assert result.volume() == pytest.approx(8.0)


def test_assert_module_children_do_not_evaluate_when_condition_fails(capsys):
    with pytest.raises(ProtoSCADError):
        evaluate_with_modules(
            'assert(false) { echo("inside"); cube(2); }',
            (AssertModule(), EchoModule(), CubeModule()),
        )
    assert capsys.readouterr().out == ""


def test_assert_guards_a_user_module():
    result = evaluate_with_modules(
        'module Box(a) { assert(a > 0, "a must be positive"); cube(a); } Box(2);',
        (AssertModule(), CubeModule()),
    )
    assert result.volume() == pytest.approx(8.0)


## =========================================================================
#  Ordinary names, not keywords


def test_echo_and_assert_are_ordinary_identifiers():
    # Unlike OpenSCAD, the words are not reserved: they name variables and
    # the calls resolve as ordinary modules (a user module of the same name
    # would shadow the builtin, like any name).
    probe = ProbeModule()
    evaluate_with_modules("echo = 5; assert = true; probe(echo);", (probe,))
    assert probe.values == [5.0]


def test_echo_and_assert_in_expression_position_are_unknown_functions():
    # The expression forms (`x = assert(cond) value;`) are OpenSCAD's and
    # stay unimplemented — see docs/MISSING_FEATURES.md, item 3.
    with pytest.raises(ProtoSCADError, match="Unknown function: 'assert'"):
        evaluate_with_modules("probe(assert(true));", MODULES)
    with pytest.raises(ProtoSCADError, match="Unknown function: 'echo'"):
        evaluate_with_modules("probe(echo(1));", MODULES)
