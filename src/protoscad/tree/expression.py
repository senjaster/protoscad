from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from protoscad.builtin_functions import lookup_builtin_function
from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.diagnostics.spans import SourceSpan
from protoscad.tree.values import (
    RangeValue,
    Type,
    ieee_div,
    ieee_fmod,
    ieee_pow,
    index_value,
    is_number,
    truthy,
    type_of,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Sequence

    from protoscad.runtime.environment import Environment


def _located(error: ProtoSCADError, span: SourceSpan | None) -> ProtoSCADError:
    """The same error with ``span`` attached, for raise sites too deep to
    know where in the source they are (typed operator helpers)."""
    if error.diagnostic.span is None and span is not None:
        return ProtoSCADError(
            error.diagnostic.message, code=error.diagnostic.code, span=span, notes=error.diagnostic.notes
        )
    return error


@dataclass(kw_only=True)
class Expression:
    """Base class for a node in the expression AST.

    ``span`` locates the node's source text for error reporting; the visitor
    fills it (``compare=False``, so node equality compares shape only).
    Hand-built or synthesized nodes (constant folding results, evaluated
    ``Literal`` re-wraps) have ``span=None``.

    Every node answers ``expression_type`` — the OpenSCAD type its
    evaluation will produce when that is decidable from the tree alone
    (``NumberLiteral`` → ``number``), and ``Type.UNKNOWN`` when runtime
    values decide (variables, indexing into vectors).
    """

    span: SourceSpan | None = field(default=None, compare=False)

    def evaluate(self, env: Environment) -> Any:
        raise NotImplementedError

    @property
    def expression_type(self) -> Type:
        return Type.UNKNOWN

    def referenced_names(self) -> set[str]:
        """The names read by this expression (its ``Variable`` leaves).

        Implemented once here by walking the dataclass fields: any field
        that is an ``Expression`` (or a list of them, or a list of
        ``Assignment``s as in ``LetExpr``) is a child subtree, so new node
        types participate automatically — as do test doubles built from
        ``Expression``. Only leaf semantics need an override (see
        ``Variable``).
        """
        names: set[str] = set()
        for entry in dataclasses.fields(self):
            value = getattr(self, entry.name)
            if isinstance(value, Expression):
                names |= value.referenced_names()
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Expression):
                        names |= item.referenced_names()
                    elif isinstance(item, Assignment):
                        names |= item.value.referenced_names()
        return names


## =========================================================================
#  Literals


@dataclass
class NumberLiteral(Expression):
    value: float

    def evaluate(self, env: Environment) -> float:
        return self.value

    @property
    def expression_type(self) -> Type:
        return Type.NUMBER


@dataclass
class StringLiteral(Expression):
    value: str

    def evaluate(self, env: Environment) -> str:
        return self.value

    @property
    def expression_type(self) -> Type:
        return Type.STRING


@dataclass
class BooleanLiteral(Expression):
    value: bool

    def evaluate(self, env: Environment) -> bool:
        return self.value

    @property
    def expression_type(self) -> Type:
        return Type.BOOLEAN


@dataclass
class UndefLiteral(Expression):
    """The ``undef`` literal — OpenSCAD's null value."""

    def evaluate(self, env: Environment) -> Any:
        return None

    @property
    def expression_type(self) -> Type:
        return Type.UNDEF


@dataclass
class VectorLiteral(Expression):
    """A vector literal, e.g. ``[12, var2+2, -3.2]``."""

    elements: list[Expression]

    def evaluate(self, env: Environment) -> list[Any]:
        return [element.evaluate(env) for element in self.elements]

    @property
    def expression_type(self) -> Type:
        return Type.VECTOR


@dataclass
class RangeLiteral(Expression):
    """A range literal: ``[start:end]`` (step 1) or ``[start:step:end]``."""

    start: Expression
    step: Expression | None
    end: Expression

    def evaluate(self, env: Environment) -> RangeValue:
        try:
            return self._range_value(
                self.start.evaluate(env),
                self.step.evaluate(env) if self.step is not None else 1.0,
                self.end.evaluate(env),
            )
        except ProtoSCADError as error:
            raise _located(error, self.span) from None

    @staticmethod
    def _range_value(start: Any, step: Any, end: Any) -> RangeValue:
        if not (is_number(start) and is_number(step) and is_number(end)):
            raise ProtoSCADError(
                f"Range bounds must be numbers, got {type_of(start).value}:{type_of(step).value}:{type_of(end).value}",
                code=ErrorCode.TYPE_ERROR,
            )
        return RangeValue(float(start), float(step), float(end))

    @property
    def expression_type(self) -> Type:
        return Type.RANGE


@dataclass
class Literal(Expression):
    """A constant value computed at the call site.

    Used to expose a bound module parameter to the module body: the argument
    expression is evaluated in the caller's scope, and the resulting value is
    wrapped here so the body sees a concrete constant rather than re-resolving
    the original (caller-scoped) expression.
    """

    value: Any

    def evaluate(self, env: Environment) -> Any:
        return self.value

    @property
    def expression_type(self) -> Type:
        return type_of(self.value)


@dataclass
class Variable(Expression):
    name: str

    def evaluate(self, env: Environment) -> Any:
        return env.lookup_variable(self.name)

    def referenced_names(self) -> set[str]:
        return {self.name}


@dataclass
class Assignment:
    """A variable binding: a name plus the expression that defines it.

    Plain data — the scoping rules (self-reference exclusion, parent lookup)
    live in ``Environment``, and the binding's source position rides on the
    value expression's ``span``.
    """

    name: str
    value: Expression


## =========================================================================
#  Typed operator semantics
#
# OpenSCAD arithmetic is defined over combinations of types (scalars, vectors,
# matrices) with IEEE-754 float behavior (1/0 is inf, 0/0 is nan). Where
# OpenSCAD answers a type mismatch with a warning and undef, we raise a
# TYPE_ERROR — the warning-to-error rule this project follows (QUIRKS.md).


def _type_error(message: str) -> ProtoSCADError:
    return ProtoSCADError(message, code=ErrorCode.TYPE_ERROR)


def _mismatch(op: str, left: Any, right: Any) -> ProtoSCADError:
    return _type_error(f"Operator {op!r} is not defined for {type_of(left).value} and {type_of(right).value}")


def _zipwise(fn: Callable[[Any, Any], Any], left: list[Any], right: list[Any]) -> list[Any]:
    # Element-wise on vectors: the result truncates to the shorter operand
    # (strict=False is the documented OpenSCAD rule), and a pair with
    # mismatched types becomes undef.
    return [_apply_pairwise(fn, a, b) for a, b in zip(left, right, strict=False)]


def _apply_pairwise(fn: Callable[[Any, Any], Any], left: Any, right: Any) -> Any:
    if is_number(left) and is_number(right):
        return fn(left, right)
    if isinstance(left, list) and isinstance(right, list):
        return _zipwise(fn, left, right)
    return None


def _scaled(fn: Callable[[Any, Any], Any], vector: list[Any], factor: Any) -> list[Any]:
    # Scalar * and / recurse into nesting levels; non-numeric leaves become undef.
    result: list[Any] = []
    for element in vector:
        if is_number(element):
            result.append(fn(element, factor))
        elif isinstance(element, list):
            result.append(_scaled(fn, element, factor))
        else:
            result.append(None)
    return result


def _negate(value: Any) -> Any:
    if is_number(value):
        return -value
    if isinstance(value, list):
        return [_negate(element) for element in value]
    return None


def _flat_numeric(vector: Any) -> bool:
    return isinstance(vector, list) and all(is_number(element) for element in vector)


def _matrix(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) > 0
        and all(isinstance(row, list) for row in value)
        and len({len(row) for row in value}) == 1
    )


def _dot(a: Sequence[Any], b: Sequence[Any]) -> float:
    # Callers check the lengths; strict= turns a violated invariant into a
    # loud failure instead of a silently truncated dot product.
    return sum(x * y for x, y in zip(a, b, strict=True))


def _columns(matrix: list[Any]) -> Iterator[tuple[Any, ...]]:
    return zip(*matrix, strict=True)


def _multiply(op: str, left: Any, right: Any) -> Any:
    if is_number(left) and is_number(right):
        return left * right
    if is_number(left) and isinstance(right, list):
        return _scaled(lambda element, factor: element * factor, right, left)
    if isinstance(left, list) and is_number(right):
        return _scaled(lambda element, factor: element * factor, left, right)
    if isinstance(left, list) and isinstance(right, list):
        if _matrix(left) and _matrix(right):
            if len(left[0]) != len(right):
                raise _mismatch(op, left, right)
            return [[_dot(row, column) for column in _columns(right)] for row in left]
        if _matrix(left) and _flat_numeric(right):
            if len(right) != len(left[0]):
                raise _mismatch(op, left, right)
            return [_dot(row, right) for row in left]
        if _flat_numeric(left) and _matrix(right):
            if len(left) != len(right):
                raise _mismatch(op, left, right)
            return [_dot(left, column) for column in _columns(right)]
        if _flat_numeric(left) and _flat_numeric(right):
            if len(left) != len(right):
                raise _mismatch(op, left, right)
            return _dot(left, right)
    raise _mismatch(op, left, right)


def _divide(op: str, left: Any, right: Any) -> Any:
    if is_number(left) and is_number(right):
        return ieee_div(left, right)
    if isinstance(left, list) and is_number(right):
        return _scaled(ieee_div, left, right)
    raise _mismatch(op, left, right)


def _modulo(op: str, left: Any, right: Any) -> Any:
    if is_number(left) and is_number(right):
        return ieee_fmod(left, right)
    raise _mismatch(op, left, right)


def _power(op: str, left: Any, right: Any) -> Any:
    if is_number(left) and is_number(right):
        return ieee_pow(left, right)
    raise _mismatch(op, left, right)


def _add_like(op: str, left: Any, right: Any, fn: Callable[[float, float], float]) -> Any:
    if is_number(left) and is_number(right):
        return fn(left, right)
    if isinstance(left, list) and isinstance(right, list):
        return _zipwise(fn, left, right)
    raise _mismatch(op, left, right)


def _coerce(value: Any) -> Any:
    # Booleans order as numbers (true=1, false=0) in comparisons.
    return float(value) if isinstance(value, bool) else value


def _ordered(op: str, left: Any, right: Any, fn: Callable[[Any, Any], bool]) -> bool:
    # Booleans order as numbers (true=1, false=0) in comparisons.
    left, right = _coerce(left), _coerce(right)
    if is_number(left) and is_number(right):
        # nan compares false to everything, as in OpenSCAD.
        return fn(left, right)
    if isinstance(left, str) and isinstance(right, str):
        return fn(left, right)
    raise _mismatch(op, left, right)


def _equals(left: Any, right: Any) -> bool:
    # Python's == already implements OpenSCAD's deep equality: booleans
    # coerce against numbers, nan equals nothing, mixed types are unequal.
    return bool(left == right)


def apply_binary(op: str, left: Any, right: Any) -> Any:
    """Evaluate a binary operator over already-evaluated operands, with
    OpenSCAD's type rules. Raises ``ProtoSCADError`` (TYPE_ERROR, or
    UNKNOWN_OPERATOR) without a span; the calling node locates it."""
    if op == "+":
        return _add_like(op, left, right, lambda a, b: a + b)
    if op == "-":
        return _add_like(op, left, right, lambda a, b: a - b)
    if op == "*":
        return _multiply(op, left, right)
    if op == "/":
        return _divide(op, left, right)
    if op == "%":
        return _modulo(op, left, right)
    if op == "^":
        return _power(op, left, right)
    if op == "<":
        return _ordered(op, left, right, lambda a, b: a < b)
    if op == "<=":
        return _ordered(op, left, right, lambda a, b: a <= b)
    if op == ">":
        return _ordered(op, left, right, lambda a, b: a > b)
    if op == ">=":
        return _ordered(op, left, right, lambda a, b: a >= b)
    if op == "==":
        return _equals(left, right)
    if op == "!=":
        return not _equals(left, right)
    if op == "&&":
        return truthy(left) and truthy(right)
    if op == "||":
        return truthy(left) or truthy(right)
    raise ProtoSCADError(f"Unknown binary operator: {op!r}", code=ErrorCode.UNKNOWN_OPERATOR)


_BINARY_OPERATORS = frozenset({"+", "-", "*", "/", "%", "^", "<", "<=", ">", ">=", "==", "!=", "&&", "||"})
_COMPARISON_OPERATORS = frozenset({"<", "<=", ">", ">=", "==", "!="})
_LOGICAL_OPERATORS = frozenset({"&&", "||"})


## =========================================================================
#  Composite expressions


@dataclass
class BinaryOp(Expression):
    op: str
    left: Expression
    right: Expression

    def __post_init__(self) -> None:
        # Resolved once: evaluate() runs on every lookup of every node.
        # An unknown operator cannot come from the grammar, so failing at
        # construction is the right place.
        if self.op not in _BINARY_OPERATORS:
            raise ProtoSCADError(f"Unknown binary operator: {self.op!r}", code=ErrorCode.UNKNOWN_OPERATOR)

    def evaluate(self, env: Environment) -> Any:
        if self.op in _LOGICAL_OPERATORS:
            # Short-circuiting keeps guarded cycles resolvable, exactly like
            # the ternary operator's laziness (see QUIRKS.md).
            left = truthy(self.left.evaluate(env))
            if self.op == "&&" and not left:
                return False
            if self.op == "||" and left:
                return True
            return truthy(self.right.evaluate(env))
        try:
            return apply_binary(self.op, self.left.evaluate(env), self.right.evaluate(env))
        except ProtoSCADError as error:
            raise _located(error, self.span) from None

    @property
    def expression_type(self) -> Type:
        left, right = self.left.expression_type, self.right.expression_type
        if self.op in _COMPARISON_OPERATORS or self.op in _LOGICAL_OPERATORS:
            return Type.BOOLEAN
        if self.op in ("+", "-"):
            if left == Type.NUMBER and right == Type.NUMBER:
                return Type.NUMBER
            if left == Type.VECTOR and right == Type.VECTOR:
                return Type.VECTOR
        elif self.op == "*":
            if left == Type.NUMBER and right == Type.NUMBER:
                return Type.NUMBER
            if Type.VECTOR in (left, right):
                return Type.VECTOR
        elif self.op == "/":
            if left == Type.NUMBER and right == Type.NUMBER:
                return Type.NUMBER
            if left == Type.VECTOR and right == Type.NUMBER:
                return Type.VECTOR
        elif self.op in ("%", "^"):
            if left == Type.NUMBER and right == Type.NUMBER:
                return Type.NUMBER
        return Type.UNKNOWN


@dataclass
class UnaryOp(Expression):
    """Prefix operators: ``-x``, ``+x`` negate/affirm element-wise over
    vectors; ``!x`` negates truthiness."""

    op: str
    operand: Expression

    def __post_init__(self) -> None:
        if self.op not in ("-", "+", "!"):
            raise ProtoSCADError(f"Unknown unary operator: {self.op!r}", code=ErrorCode.UNKNOWN_OPERATOR)

    def evaluate(self, env: Environment) -> Any:
        value = self.operand.evaluate(env)
        if self.op == "!":
            return not truthy(value)
        if not (is_number(value) or isinstance(value, list)):
            raise _located(_mismatch(self.op, value, value), self.span)
        return _negate(value) if self.op == "-" else value

    @property
    def expression_type(self) -> Type:
        if self.op == "!":
            return Type.BOOLEAN
        operand = self.operand.expression_type
        return operand if operand in (Type.NUMBER, Type.VECTOR) else Type.UNKNOWN


@dataclass
class TernaryOp(Expression):
    """``condition ? then_expr : else_expr`` — only the taken branch is
    evaluated, which is what lets a condition break a variable cycle."""

    condition: Expression
    then_expr: Expression
    else_expr: Expression

    def evaluate(self, env: Environment) -> Any:
        branch = self.then_expr if truthy(self.condition.evaluate(env)) else self.else_expr
        return branch.evaluate(env)

    @property
    def expression_type(self) -> Type:
        then_type, else_type = self.then_expr.expression_type, self.else_expr.expression_type
        return then_type if then_type == else_type else Type.UNKNOWN


@dataclass
class Index(Expression):
    """``collection[index]`` — vectors and strings are indexable."""

    collection: Expression
    index: Expression

    def evaluate(self, env: Environment) -> Any:
        try:
            return index_value(self.collection.evaluate(env), self.index.evaluate(env))
        except ProtoSCADError as error:
            raise _located(error, self.span) from None

    @property
    def expression_type(self) -> Type:
        # Indexing a string yields a one-character string; vector element
        # types are not statically known.
        return Type.STRING if self.collection.expression_type == Type.STRING else Type.UNKNOWN


@dataclass
class Call(Expression):
    """A call to a builtin function, e.g. ``sin(a) + 2``.

    User-defined functions and function-holding variables do not exist yet;
    when they land (see NAMESPACES.md) the lookup here grows a variable and
    function scope walk ahead of the builtin registry.
    """

    name: str
    args: list[Expression]

    def evaluate(self, env: Environment) -> Any:
        function = lookup_builtin_function(self.name)
        if function is None:
            raise ProtoSCADError(f"Unknown function: {self.name!r}", code=ErrorCode.UNKNOWN_FUNCTION, span=self.span)
        values = [argument.evaluate(env) for argument in self.args]
        try:
            return function.call(values)
        except ProtoSCADError as error:
            raise _located(error, self.span) from None


@dataclass
class LetExpr(Expression):
    """``let(name = value, ...) body`` as an expression: the body evaluates
    in a scope extended with the bindings (the same declarative, lazy
    semantics as the ``let`` statement)."""

    bindings: list[Assignment]
    body: Expression

    def evaluate(self, env: Environment) -> Any:
        scope = env.extend()
        for binding in self.bindings:
            scope.add_variable(binding.name, binding)
        return self.body.evaluate(scope)

    @property
    def expression_type(self) -> Type:
        return self.body.expression_type


@dataclass
class Paren(Expression):
    inner: Expression

    def evaluate(self, env: Environment) -> Any:
        return self.inner.evaluate(env)

    @property
    def expression_type(self) -> Type:
        return self.inner.expression_type


@dataclass
class Undefined(Expression):
    """The value of a module parameter that has no default and was not bound.

    A required parameter left unbound is rejected at bind time (see
    ``ModuleDefinition.bind_args``) with the call site in the error, so
    reaching this evaluation is a leaked sentinel — the backstop keeps it a
    reported failure rather than a crash.
    """

    def evaluate(self, env: Environment) -> Any:
        raise ProtoSCADError("Undefined parameter value", code=ErrorCode.MISSING_REQUIRED_PARAMETER)


## =========================================================================
#  Constant folding


def _constant(node: Expression) -> tuple[bool, Any]:
    """Whether ``node`` is a constant, and its Python value if so."""
    if isinstance(node, NumberLiteral | Literal | StringLiteral | BooleanLiteral):
        return True, node.value
    if isinstance(node, UndefLiteral):
        return True, None
    return False, None


def fold(node: Expression) -> Expression:
    """Constant-fold an expression subtree, bottom-up.

    Literal-only arithmetic collapses to a single literal, an vector of
    constants to a ``Literal`` list, and a constant ternary/index/range to
    its constant result — the shapes real .scad files are full of
    (``[6, 10, 10]``, ``$fn/4 + 2``). Arithmetic on two number literals
    stays a ``NumberLiteral``. Folding is best-effort: an operation that
    would fail at run time (``[1]+2``) is left unfolded, so the error
    surfaces at evaluation, in context. Replacement nodes inherit the
    original's ``span``.
    """
    if isinstance(node, BinaryOp):
        left, right = fold(node.left), fold(node.right)
        left_constant, left_value = _constant(left)
        right_constant, right_value = _constant(right)
        if left_constant and right_constant:
            try:
                value = apply_binary(node.op, left_value, right_value)
            except Exception:
                # Folding must never fail construction on an unfoldable
                # operation.
                return BinaryOp(node.op, left, right, span=node.span)
            if isinstance(value, bool):
                return BooleanLiteral(value, span=node.span)
            if is_number(value):
                if isinstance(left, NumberLiteral) and isinstance(right, NumberLiteral):
                    return NumberLiteral(value, span=node.span)
                return Literal(value, span=node.span)
            return Literal(value, span=node.span)
        return BinaryOp(node.op, left, right, span=node.span)
    if isinstance(node, UnaryOp):
        operand = fold(node.operand)
        operand_constant, value = _constant(operand)
        if operand_constant:
            if node.op == "!":
                return BooleanLiteral(not truthy(value), span=node.span)
            if is_number(value) or isinstance(value, list):
                if node.op == "+":
                    return operand
                result = _negate(value)
                if isinstance(operand, NumberLiteral) and is_number(result):
                    return NumberLiteral(result, span=node.span)
                return Literal(result, span=node.span)
        return UnaryOp(node.op, operand, span=node.span)
    if isinstance(node, TernaryOp):
        condition = fold(node.condition)
        condition_constant, value = _constant(condition)
        if condition_constant:
            # Only the taken branch participates — folding must not lose
            # the ternary's laziness.
            return fold(node.then_expr if truthy(value) else node.else_expr)
        return TernaryOp(
            condition,
            fold(node.then_expr),
            fold(node.else_expr),
            span=node.span,
        )
    if isinstance(node, Index):
        collection, index = fold(node.collection), fold(node.index)
        collection_constant, collection_value = _constant(collection)
        index_constant, index_constant_value = _constant(index)
        if collection_constant and index_constant:
            try:
                value = index_value(collection_value, index_constant_value)
            except Exception:
                return Index(collection, index, span=node.span)
            if isinstance(collection_value, str):
                return StringLiteral(value, span=node.span)
            return Literal(value, span=node.span)
        return Index(collection, index, span=node.span)
    if isinstance(node, RangeLiteral):
        start = fold(node.start)
        step = fold(node.step) if node.step is not None else None
        end = fold(node.end)
        candidates: list[tuple[bool, Any]] = [
            _constant(start),
            _constant(step) if step is not None else (True, 1.0),
            _constant(end),
        ]
        if all(is_constant for is_constant, _ in candidates):
            values = [value for _, value in candidates]
            try:
                if not all(is_number(value) for value in values):
                    raise TypeError("non-numeric range bound")
                return Literal(RangeValue(*(float(value) for value in values)), span=node.span)
            except Exception:
                pass  # zero step or non-numeric bound: the error surfaces at evaluation
        return RangeLiteral(start, step, end, span=node.span)
    if isinstance(node, Paren):
        inner = fold(node.inner)
        is_constant, _ = _constant(inner)
        return inner if is_constant else Paren(inner, span=node.span)
    if isinstance(node, VectorLiteral):
        elements = [fold(element) for element in node.elements]
        constants = [_constant(element) for element in elements]
        if all(is_constant for is_constant, _ in constants):
            return Literal([value for _, value in constants], span=node.span)
        return VectorLiteral(elements, span=node.span)
    if isinstance(node, LetExpr):
        bindings = [Assignment(binding.name, fold(binding.value)) for binding in node.bindings]
        return LetExpr(bindings, fold(node.body), span=node.span)
    return node
