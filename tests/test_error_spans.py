from __future__ import annotations

import pytest

from protoscad.builtins.cube import CubeModule
from protoscad.diagnostics import ErrorCode, ProtoSCADError, SourceSpan
from protoscad.parser import parse_scad
from protoscad.runtime.evaluator import evaluate
from protoscad.runtime.resolver import OpenScadResolver

# Sources below put each statement on its own line, so statement spans start
# at column 0 and the expected SourceSpan values are easy to read: a module
# call's span excludes the trailing ';', a binding's span includes it.
# Argument errors point at the offending argument expression, so their spans
# are the argument's columns within the call.
CYCLE_SOURCE = """\
x = 1;
y = x;
x = y + 1;
cube(x);
"""


def evaluate_source(source: str, resolver=None):
    return evaluate(parse_scad(source), [CubeModule()], resolver=resolver)


def test_unknown_module_error_carries_call_span():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_source("cube(1);\nsphare(2);\n")
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.UNKNOWN_MODULE
    assert diagnostic.span == SourceSpan(2, 0, 2, 9)


def test_missing_required_parameter_error_carries_call_span():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_source("cube();\n")
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.MISSING_REQUIRED_PARAMETER
    assert diagnostic.message == "Missing required parameter 'size' for module 'cube'"
    assert diagnostic.span == SourceSpan(1, 0, 1, 6)


def test_unknown_parameter_error_points_at_the_argument():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_source("cube(size = 1, bogus = 2);\n")
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.UNKNOWN_PARAMETER
    # The offending `bogus = 2` argument.
    assert diagnostic.span == SourceSpan(1, 15, 1, 24)


def test_too_many_positional_args_error_points_at_first_excess_argument():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_source("cube(1, 2, 3);\n")
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.TOO_MANY_POSITIONAL_ARGS
    # The first argument beyond the parameter list: `3`.
    assert diagnostic.span == SourceSpan(1, 11, 1, 12)


def test_unknown_variable_error_carries_binding_span():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_source("q = zz;\ncube(1);\n")
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.UNKNOWN_VARIABLE
    assert diagnostic.span == SourceSpan(1, 0, 1, 7)


def test_use_before_assignment_error_carries_binding_span():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_source("y = x;\nx = 10;\ncube(y);\n", resolver=OpenScadResolver())
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.USE_BEFORE_ASSIGNMENT
    assert diagnostic.span == SourceSpan(1, 0, 1, 6)


def test_lazy_cycle_error_carries_definition_span():
    # The cycle is forced when `cube(x)` reads x; the error points at x's
    # defining expression (`y + 1`), not at the read.
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_source(CYCLE_SOURCE)
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.CIRCULAR_DEPENDENCY
    assert diagnostic.span == SourceSpan(3, 4, 3, 9)


def test_openscad_cycle_error_carries_definition_span():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_source(CYCLE_SOURCE, resolver=OpenScadResolver())
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.CIRCULAR_DEPENDENCY
    assert diagnostic.span == SourceSpan(3, 0, 3, 10)
