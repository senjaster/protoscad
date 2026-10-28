"""The builtin function registry (``sin``, ``len``, ``str``, ...).

Functions live outside ``builtins/`` on purpose: that package holds builtin
*modules* and imports the runtime, while expressions must be able to reach
functions without a cycle. When user-defined functions land (NAMESPACES.md)
the call-position lookup grows scope walks ahead of this registry.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.tree.values import Type, format_value, ieee_pow, type_of


@dataclass(frozen=True)
class Signature:
    """One acceptable argument shape: fixed parameter types plus an
    optional repeatable trailing type. ``Type.ANY`` matches any value."""

    parameters: tuple[Type, ...]
    variadic: Type | None = None

    def __str__(self) -> str:
        rendered = ", ".join(parameter.value for parameter in self.parameters)
        if self.variadic is not None:
            rendered = f"{rendered}, {self.variadic.value}..." if rendered else f"{self.variadic.value}..."
        return rendered

    def accepts(self, arg_types: Sequence[Type]) -> bool:
        if len(arg_types) < len(self.parameters):
            return False
        if self.variadic is None and len(arg_types) > len(self.parameters):
            return False
        for expected, actual in zip(self.parameters, arg_types, strict=False):
            if expected is not Type.ANY and expected is not actual:
                return False
        if self.variadic is not None:
            return all(self.variadic is Type.ANY or t == self.variadic for t in arg_types[len(self.parameters) :])
        return True


@dataclass(frozen=True)
class BuiltinFunction:
    """A callable value identified by name, with typed signatures.

    OpenSCAD answers bad builtin calls with ``undef`` and a warning; as
    elsewhere in this project, we raise instead (INVALID_ARGUMENT).
    """

    name: str
    signatures: tuple[Signature, ...]
    implementation: Callable[..., Any] = field(compare=False)

    def call(self, args: list[Any]) -> Any:
        arg_types = [type_of(arg) for arg in args]
        if not any(signature.accepts(arg_types) for signature in self.signatures):
            rendered = ", ".join(t.value for t in arg_types) if arg_types else "no arguments"
            expected = " or ".join(str(signature) for signature in self.signatures)
            raise ProtoSCADError(
                f"{self.name}({rendered}) matches no signature (expected {expected})",
                code=ErrorCode.INVALID_ARGUMENT,
            )
        return self.implementation(*args)


def _require_numbers(vector: list[Any], name: str) -> None:
    for element in vector:
        if type_of(element) is not Type.NUMBER:
            raise ProtoSCADError(
                f"{name}() expects a numeric vector, found {type_of(element).value} element",
                code=ErrorCode.INVALID_ARGUMENT,
            )


## Trigonometry — degrees, as in OpenSCAD


def _asin(x: float) -> float:
    try:
        return math.degrees(math.asin(x))
    except ValueError:
        return math.nan


def _acos(x: float) -> float:
    try:
        return math.degrees(math.acos(x))
    except ValueError:
        return math.nan


## Powers, roots and logs — C double semantics (nan/inf, never errors)


def _sqrt(x: float) -> float:
    try:
        return math.sqrt(x)
    except ValueError:
        return math.nan


def _exp(x: float) -> float:
    try:
        return math.exp(x)
    except OverflowError:
        return math.inf


def _ln(x: float) -> float:
    if x == 0:
        return -math.inf
    if x < 0:
        return math.nan
    return math.log(x)


def _log(x: float) -> float:
    if x == 0:
        return -math.inf
    if x < 0:
        return math.nan
    return math.log10(x)


## Rounding — round is half-away-from-zero, unlike Python's banker's rounding


def _round(x: float) -> float:
    return float(math.floor(x + 0.5)) if x >= 0 else float(math.ceil(x - 0.5))


def _sign(x: float) -> float:
    return 0.0 if x == 0 else math.copysign(1.0, x)


## Vector and string functions


def _min(*args: Any) -> float:
    if len(args) == 1:
        _require_numbers(args[0], "min")
        return min(args[0])
    return min(args)


def _max(*args: Any) -> float:
    if len(args) == 1:
        _require_numbers(args[0], "max")
        return max(args[0])
    return max(args)


def _norm(vector: list[Any]) -> float:
    _require_numbers(vector, "norm")
    return math.sqrt(sum(x * x for x in vector))


def _cross(a: list[Any], b: list[Any]) -> Any:
    _require_numbers(a, "cross")
    _require_numbers(b, "cross")
    if len(a) == 2 and len(b) == 2:
        return a[0] * b[1] - a[1] * b[0]
    if len(a) == 3 and len(b) == 3:
        return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    raise ProtoSCADError("cross() expects 2D or 3D numeric vectors", code=ErrorCode.INVALID_ARGUMENT)


def _concat(*args: Any) -> list[Any]:
    # Vectors lose one nesting level; scalars and strings append as elements.
    result: list[Any] = []
    for arg in args:
        if isinstance(arg, list):
            result.extend(arg)
        else:
            result.append(arg)
    return result


def _str(*args: Any) -> str:
    return "".join(format_value(arg) for arg in args)


def _chr(*codes: float) -> str:
    try:
        return "".join(chr(int(code)) for code in codes)
    except ValueError, OverflowError:
        raise ProtoSCADError("chr() code point out of range", code=ErrorCode.INVALID_ARGUMENT) from None


def _ord(s: str) -> Any:
    return float(ord(s)) if len(s) == 1 else [float(ord(ch)) for ch in s]


def _rands(low: float, high: float, count: float, seed: float | None = None) -> list[float]:
    if count != math.floor(count) or count < 0:
        raise ProtoSCADError("rands() count must be a non-negative integer", code=ErrorCode.INVALID_ARGUMENT)
    rng = random.Random(seed)
    return [rng.uniform(low, high) for _ in range(int(count))]


_N = Type.NUMBER


def _single(name: str, implementation: Callable[[Any], Any], parameter: Type) -> BuiltinFunction:
    return BuiltinFunction(name, (Signature((parameter,)),), implementation)


def _trig(name: str, fn: Callable[[float], float]) -> BuiltinFunction:
    return BuiltinFunction(name, (Signature((_N,)),), fn)


_FUNCTIONS = [
    _trig("sin", lambda x: math.sin(math.radians(x))),
    _trig("cos", lambda x: math.cos(math.radians(x))),
    _trig("tan", lambda x: math.tan(math.radians(x))),
    _trig("asin", _asin),
    _trig("acos", _acos),
    _trig("atan", lambda x: math.degrees(math.atan(x))),
    BuiltinFunction("atan2", (Signature((_N, _N)),), lambda y, x: math.degrees(math.atan2(y, x))),
    BuiltinFunction("pow", (Signature((_N, _N)),), ieee_pow),
    BuiltinFunction("sqrt", (Signature((_N,)),), _sqrt),
    BuiltinFunction("exp", (Signature((_N,)),), _exp),
    BuiltinFunction("ln", (Signature((_N,)),), _ln),
    BuiltinFunction("log", (Signature((_N,)),), _log),
    _trig("abs", abs),
    _trig("sign", _sign),
    _trig("floor", lambda x: float(math.floor(x))),
    _trig("ceil", lambda x: float(math.ceil(x))),
    _trig("round", _round),
    BuiltinFunction("min", (Signature((_N, _N), variadic=_N), Signature((Type.VECTOR,))), _min),
    BuiltinFunction("max", (Signature((_N, _N), variadic=_N), Signature((Type.VECTOR,))), _max),
    BuiltinFunction("len", (Signature((Type.VECTOR,)), Signature((Type.STRING,))), lambda v: float(len(v))),
    BuiltinFunction("norm", (Signature((Type.VECTOR,)),), _norm),
    BuiltinFunction("cross", (Signature((Type.VECTOR, Type.VECTOR)),), _cross),
    BuiltinFunction("concat", (Signature((), variadic=Type.ANY),), _concat),
    BuiltinFunction("str", (Signature((), variadic=Type.ANY),), _str),
    BuiltinFunction("chr", (Signature((), variadic=_N),), _chr),
    BuiltinFunction("ord", (Signature((Type.STRING,)),), _ord),
    BuiltinFunction("rands", (Signature((_N, _N, _N)), Signature((_N, _N, _N, _N))), _rands),
    _single("is_undef", lambda v: v is None, Type.ANY),
    _single("is_list", lambda v: isinstance(v, list), Type.ANY),
    _single("is_num", lambda v: type_of(v) is Type.NUMBER, Type.ANY),
    _single("is_bool", lambda v: type_of(v) is Type.BOOLEAN, Type.ANY),
    _single("is_string", lambda v: type_of(v) is Type.STRING, Type.ANY),
]

BUILTIN_FUNCTIONS: dict[str, BuiltinFunction] = {function.name: function for function in _FUNCTIONS}

BUILTIN_CONSTANTS: dict[str, float] = {"PI": math.pi}


def lookup_builtin_function(name: str) -> BuiltinFunction | None:
    return BUILTIN_FUNCTIONS.get(name)
