from __future__ import annotations

import math
from typing import Any

import pytest

from protoscad.builtin_functions import BUILTIN_FUNCTIONS, lookup_builtin_function
from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.runtime.environment import Environment
from protoscad.tree.expression import Call, Expression, Literal, NumberLiteral, StringLiteral

_ENV = Environment()


def evaluate_call(name: str, *args: object) -> Any:
    """Call a builtin with Python values, wrapping them as constant nodes."""
    wrapped: list[Expression] = []
    for arg in args:
        if isinstance(arg, Expression):
            wrapped.append(arg)
        elif isinstance(arg, list):
            wrapped.append(Literal(arg))
        elif isinstance(arg, str):
            wrapped.append(StringLiteral(arg))
        elif arg is None:
            wrapped.append(Literal(None))
        else:
            wrapped.append(NumberLiteral(float(arg)))  # type: ignore[arg-type]
    return Call(name, wrapped).evaluate(_ENV)


## =========================================================================
#  Registry


def test_registry_covers_the_math_and_string_core():
    expected = {
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "atan2",
        "abs",
        "sign",
        "sqrt",
        "pow",
        "exp",
        "ln",
        "log",
        "floor",
        "ceil",
        "round",
        "min",
        "max",
        "len",
        "norm",
        "cross",
        "concat",
        "str",
        "chr",
        "ord",
        "rands",
        "is_undef",
        "is_list",
        "is_num",
        "is_bool",
        "is_string",
    }
    assert expected == set(BUILTIN_FUNCTIONS)
    assert lookup_builtin_function("nope") is None


## =========================================================================
#  Trigonometry is in degrees


@pytest.mark.parametrize(
    "call,expected",
    [
        (("sin", 90.0), 1.0),
        (("cos", 180.0), -1.0),
        (("tan", 45.0), 1.0),
        (("asin", 1.0), 90.0),
        (("acos", 1.0), 0.0),
        (("atan", 1.0), 45.0),
        (("atan2", 5.0, -5.0), 135.0),
    ],
)
def test_trigonometry_in_degrees(call, expected):
    assert evaluate_call(*call) == pytest.approx(expected)


def test_inverse_trig_domain_error_is_nan():
    assert math.isnan(evaluate_call("asin", 2.0))


## =========================================================================
#  Numbers


@pytest.mark.parametrize(
    "call,expected",
    [
        (("abs", -2.5), 2.5),
        (("sign", -3.0), -1.0),
        (("sign", 0.0), 0.0),
        (("floor", -4.4), -5.0),
        (("ceil", -4.4), -4.0),
        (("pow", 125.0, 1.0 / 3.0), 5.0),
        (("sqrt", 9.0), 3.0),
        (("exp", 0.0), 1.0),
        (("ln", math.e), 1.0),
        (("log", 1000.0), 3.0),
    ],
)
def test_number_functions(call, expected):
    assert evaluate_call(*call) == pytest.approx(expected)


def test_round_is_half_away_from_zero():
    assert evaluate_call("round", 5.5) == 6.0
    assert evaluate_call("round", -5.5) == -6.0
    assert evaluate_call("round", 2.5) == 3.0


def test_min_max_scalars_and_vector_form():
    assert evaluate_call("min", 3.0, 1.0, 2.0) == 1.0
    assert evaluate_call("max", 3.0, 1.0, 2.0) == 3.0
    assert evaluate_call("min", [3.0, 1.0, 2.0]) == 1.0
    assert evaluate_call("max", [3.0, 1.0, 2.0]) == 3.0


def test_domain_edge_cases_follow_c_doubles():
    assert math.isnan(evaluate_call("sqrt", -1.0))
    assert evaluate_call("ln", 0.0) == -math.inf
    assert evaluate_call("exp", 1000.0) == math.inf


## =========================================================================
#  Vectors and strings


def test_len_of_vector_and_string():
    assert evaluate_call("len", [1.0, 2.0, 3.0]) == 3.0
    assert evaluate_call("len", StringLiteral("abc")) == 3.0


def test_norm_and_cross():
    assert evaluate_call("norm", [3.0, 4.0]) == 5.0
    assert evaluate_call("norm", []) == 0.0
    assert evaluate_call("cross", [1.0, 0.0], [0.0, 1.0]) == 1.0  # 2D: z scalar
    assert evaluate_call("cross", [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]) == [0.0, 0.0, 1.0]


def test_cross_wrong_dimensions_raise():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_call("cross", [1.0], [1.0])
    assert excinfo.value.diagnostic.code == ErrorCode.INVALID_ARGUMENT


def test_concat_flattens_one_level_and_appends_scalars():
    assert evaluate_call("concat", [1.0, 2.0], 3.0, "a") == [1.0, 2.0, 3.0, "a"]
    # Strings append as elements, they do not merge (that is str's job).
    assert evaluate_call("concat", StringLiteral("abc"), StringLiteral("def")) == ["abc", "def"]


def test_str_concatenates_formatted_values():
    assert evaluate_call("str", NumberLiteral(1.0), StringLiteral("x"), [2.0]) == "1x[2]"
    assert evaluate_call("str") == ""


def test_chr_and_ord():
    assert evaluate_call("chr", 65.0) == "A"
    assert evaluate_call("chr", 72.0, 105.0) == "Hi"
    assert evaluate_call("ord", StringLiteral("A")) == 65.0
    assert evaluate_call("ord", StringLiteral("Hi")) == [72.0, 105.0]


def test_rands_is_seedable_and_half_open():
    values = evaluate_call("rands", 1.0, 2.0, 5.0, 42.0)
    assert len(values) == 5
    assert all(1.0 <= v < 2.0 for v in values)
    assert evaluate_call("rands", 1.0, 2.0, 5.0, 42.0) == values  # same seed, same stream


def test_type_tests():
    assert evaluate_call("is_undef", StringLiteral("x")) is False
    assert evaluate_call("is_list", [1.0]) is True
    # Booleans are not numbers in OpenSCAD's type tests
    assert evaluate_call("is_num", NumberLiteral(1.0)) is True
    assert evaluate_call("is_bool", NumberLiteral(1.0)) is False
    assert evaluate_call("is_string", StringLiteral("x")) is True


## =========================================================================
#  Signature checking


def test_wrong_type_raises_invalid_argument():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_call("sin", StringLiteral("a"))
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code == ErrorCode.INVALID_ARGUMENT
    assert "sin(string)" in diagnostic.message
    assert "number" in diagnostic.message


def test_wrong_arity_raises_invalid_argument():
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_call("atan2", 1.0)
    assert excinfo.value.diagnostic.code == ErrorCode.INVALID_ARGUMENT


def test_signature_rendering_includes_variadic():
    assert str(BUILTIN_FUNCTIONS["min"].signatures[0]) == "number, number, number..."
    assert str(BUILTIN_FUNCTIONS["str"].signatures[0]) == "any..."
    assert str(BUILTIN_FUNCTIONS["pow"].signatures[0]) == "number, number"


def test_undef_argument_does_not_match_typed_signature():
    # Passing undef where a number is expected is a signature mismatch —
    # OpenSCAD would warn and answer undef.
    with pytest.raises(ProtoSCADError):
        evaluate_call("sqrt", None)
