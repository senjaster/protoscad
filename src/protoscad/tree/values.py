"""The runtime value model: the six OpenSCAD value types, range values,
IEEE-754 arithmetic helpers and value formatting.

Expressions evaluate to plain Python values (``float``, ``bool``, ``str``,
``list``, ``None`` for ``undef``, :class:`RangeValue` for ranges); this
module is the single place that knows which Python shapes represent which
OpenSCAD types and what the type is called in a message.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from protoscad.diagnostics import ErrorCode, ProtoSCADError


class Type(StrEnum):
    """The OpenSCAD value types, plus two pattern-only members.

    ``UNKNOWN`` marks a type that cannot be decided statically (a variable,
    an index into a vector); ``ANY`` never describes a value — it is a
    wildcard used in builtin-function signatures.
    """

    UNDEF = "undef"
    NUMBER = "number"
    BOOLEAN = "boolean"
    STRING = "string"
    VECTOR = "vector"
    RANGE = "range"
    FUNCTION = "function"
    UNKNOWN = "unknown"
    ANY = "any"


def type_of(value: Any) -> Type:
    """The OpenSCAD type of a runtime value."""
    if value is None:
        return Type.UNDEF
    # bool before the numeric check: bool is an int subclass in Python,
    # but a distinct value type in OpenSCAD.
    if isinstance(value, bool):
        return Type.BOOLEAN
    if isinstance(value, int | float):
        return Type.NUMBER
    if isinstance(value, str):
        return Type.STRING
    if isinstance(value, RangeValue):
        return Type.RANGE
    if isinstance(value, list):
        return Type.VECTOR
    if callable(value):
        return Type.FUNCTION
    return Type.UNKNOWN


def is_number(value: Any) -> bool:
    """Whether ``value`` is an OpenSCAD number (booleans excluded)."""
    return isinstance(value, int | float) and not isinstance(value, bool)


def truthy(value: Any) -> bool:
    """OpenSCAD truthiness: false, 0, -0, "", [], undef are false;
    everything else — including nan and [false] — is true."""
    # Python's bool() agrees on exactly this set for the values we model.
    return bool(value)


@dataclass(frozen=True)
class RangeValue:
    """The value of ``[start:step:end]`` — end included when reachable.

    Ranges are values in their own right (``for`` iterates them); they are
    deliberately not lists, matching OpenSCAD's "ranges are not vectors".
    """

    start: float
    step: float
    end: float

    def __post_init__(self) -> None:
        if self.step == 0:
            raise ProtoSCADError("Range step must not be zero", code=ErrorCode.TYPE_ERROR)

    @property
    def length(self) -> int:
        """Number of elements: empty when the step walks away from the end."""
        if (self.step > 0 and self.end < self.start) or (self.step < 0 and self.end > self.start):
            return 0
        # Relative epsilon: [0:0.5:5] must count as exactly 11 elements
        # although (5-0)/0.5 computes to 10.000000000000002.
        quotient = (self.end - self.start) / self.step
        return math.floor(quotient * (1 + 1e-10)) + 1

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> Any:
        for index in range(self.length):
            # Multiplying (rather than accumulating) keeps drift bounded.
            yield self.start + index * self.step

    def __str__(self) -> str:
        if self.step == 1:
            return f"[{format_value(self.start)}:{format_value(self.end)}]"
        return f"[{format_value(self.start)}:{format_value(self.step)}:{format_value(self.end)}]"


def format_value(value: Any) -> str:
    """Render a value the way ``echo``/``str()`` print it: integral numbers
    without a decimal part, booleans as ``true``/``false``, ``None`` as
    ``undef``, vectors bracketed."""
    if value is None:
        return "undef"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return _format_number(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, RangeValue):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(format_value(element) for element in value) + "]"
    return str(value)


def _format_number(value: float) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf" if value > 0 else "-inf"
    if value.is_integer():
        return str(int(value))
    return str(value)


# --- IEEE-754 arithmetic -----------------------------------------------------
#
# OpenSCAD numbers are C doubles: division by zero is inf/nan, never an
# error. Python's operators raise instead, so arithmetic goes through these
# helpers.


def ieee_div(left: float, right: float) -> float:
    if right == 0.0:
        if left == 0.0 or math.isnan(left):
            return math.nan
        sign = math.copysign(1.0, left) * math.copysign(1.0, right)
        return math.inf * sign
    return left / right


def ieee_fmod(left: float, right: float) -> float:
    # C fmod: the result keeps the dividend's sign, x % 0 is nan.
    if right == 0.0:
        return math.nan
    return math.fmod(left, right)


def ieee_pow(left: float, right: float) -> float:
    try:
        return math.pow(left, right)
    except OverflowError:
        return math.inf
    except ValueError:
        # C pow: 0 raised to a negative power is inf, negative bases with
        # fractional exponents are nan.
        if left == 0.0 and right < 0:
            return math.inf
        return math.nan


def index_value(collection: Any, index: Any) -> Any:
    """``collection[index]`` with OpenSCAD semantics: the index must be an
    integer number; strings yield one-character strings.

    OpenSCAD answers out-of-range indexing with ``undef`` and a warning —
    as elsewhere, we raise instead (see QUIRKS.md's warning-to-error rule).
    """
    if not is_number(index) or not math.isfinite(index) or index != math.floor(index):
        raise ProtoSCADError(
            f"Index must be an integer number, got {type_of(index).value}", code=ErrorCode.INVALID_INDEX
        )
    position = int(index)
    if isinstance(collection, list | str):
        if 0 <= position < len(collection):
            return collection[position]
        raise ProtoSCADError(
            f"Index {format_value(index)} out of range for {type_of(collection).value} of length {len(collection)}",
            code=ErrorCode.INDEX_OUT_OF_RANGE,
        )
    raise ProtoSCADError(f"{type_of(collection).value.capitalize()} is not indexable", code=ErrorCode.TYPE_ERROR)


_SIMPLE_ESCAPES = {"t": "\t", "n": "\n", "r": "\r", '"': '"', "\\": "\\"}


def unescape_string(raw: str) -> str:
    """Decode the escapes of a string literal body (quotes already stripped):
    ``\\t \\n \\r \\" \\\\ \\xHH \\uHHHH \\UHHHHHH``."""
    result: list[str] = []
    position = 0
    while position < len(raw):
        char = raw[position]
        if char != "\\":
            result.append(char)
            position += 1
            continue
        if position + 1 >= len(raw):
            raise ProtoSCADError("Unterminated escape sequence in string literal", code=ErrorCode.SYNTAX)
        escape = raw[position + 1]
        if escape in _SIMPLE_ESCAPES:
            result.append(_SIMPLE_ESCAPES[escape])
            position += 2
        elif escape in ("x", "u", "U"):
            digits = {"x": 2, "u": 4, "U": 6}[escape]
            hex_part = raw[position + 2 : position + 2 + digits]
            if len(hex_part) != digits or any(c not in "0123456789abcdefABCDEF" for c in hex_part):
                raise ProtoSCADError(
                    f"Invalid \\{escape} escape: expected {digits} hexadecimal digits",
                    code=ErrorCode.SYNTAX,
                )
            result.append(chr(int(hex_part, 16)))
            position += 2 + digits
        else:
            raise ProtoSCADError(f"Unknown escape sequence '\\{escape}'", code=ErrorCode.SYNTAX)
    return "".join(result)
