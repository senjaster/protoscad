from __future__ import annotations

from typing import Any, Mapping

import pytest
from manifold3d import Manifold

from manifold_learn.ast.evaluator import TreeEvaluator
from manifold_learn.ast.expression import Assignment, NumberLiteral
from manifold_learn.ast.module_definition import BuiltinModule, ChildInvocation, EvalContext
from manifold_learn.ast.manifold import CubeModule, TranslateModule
from conftest import parse_scad

MARKER_GEOMETRY = Manifold.cube([1.0, 1.0, 1.0])


class RecordingModule(BuiltinModule):
    """Test double: records evaluated args, returns a marker geometry."""

    def __init__(self, name: str, required=("value",)):
        self._name = name
        self._parameters = self.make_parameters(required=required)
        self.calls: list[dict[str, Any]] = []

    def instantiate(self, ctx: EvalContext) -> Manifold:
        self.calls.append(dict(ctx.args))
        return MARKER_GEOMETRY

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self._parameters


class ForLoopModule(BuiltinModule):
    """Demonstrates the instantiate contract: an ordinary builtin can
    re-evaluate its body once per value with a fresh binding."""

    def instantiate(self, ctx: EvalContext) -> list[Manifold]:
        results = []
        for value in ctx.args["values"]:
            env = ctx.env.extend({"i": Assignment("i", NumberLiteral(value))})
            for invocation in ctx.children:
                results.append(ctx.evaluate(ChildInvocation(invocation.node, env)))
        return results

    @property
    def name(self) -> str:
        return "for"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("values",))


def evaluate_with_modules(source: str, modules):
    tree = parse_scad(source)
    return TreeEvaluator(modules).evaluate(tree)


def test_top_level_assignment_visible_to_module_args():
    probe = RecordingModule("probe")
    evaluate_with_modules("width = 10; probe(width);", [probe])
    assert probe.calls == [{"value": 10.0}]


def test_last_assignment_wins_for_whole_scope():
    probe = RecordingModule("probe")
    evaluate_with_modules("width = 10; width = 100; probe(width);", [probe])
    assert probe.calls == [{"value": 100.0}]


def test_lazy_assignment_reflects_final_scope_values():
    # Assignments are evaluated lazily against the final scope state, so
    # depth sees the redefined width (known deviation from OpenSCAD's
    # eager capture, preserved from the previous evaluator).
    probe = RecordingModule("probe")
    evaluate_with_modules("width = 10; depth = width * 2; width = 100; probe(depth);", [probe])
    assert probe.calls == [{"value": 200.0}]


def test_let_binding_visible_to_children():
    probe = RecordingModule("probe")
    result = evaluate_with_modules("let(offset = 4) { probe(offset); }", [probe])
    assert probe.calls == [{"value": 4.0}]
    assert result.volume() == pytest.approx(1.0)


def test_let_binding_not_visible_outside():
    probe = RecordingModule("probe")
    evaluate_with_modules("let(offset = 4) { probe(1); } probe(offset);", [probe])
    assert probe.calls == [{"value": 1.0}, {"value": None}]


def test_block_variable_scopes_to_block():
    probe = RecordingModule("probe")
    evaluate_with_modules("{ local = 7; probe(local); } probe(local);", [probe])
    assert probe.calls == [{"value": 7.0}, {"value": None}]


def test_block_shadowing_references_parent_on_rhs():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "width = 100; { width = width / 2; probe(width); } probe(width);",
        [probe],
    )
    assert probe.calls == [{"value": 50.0}, {"value": 100.0}]


def test_sibling_does_not_see_let_binding():
    probe = RecordingModule("probe")
    evaluate_with_modules("let(x = 1) probe(1); probe(x);", [probe])
    assert probe.calls == [{"value": 1.0}, {"value": None}]


def test_multiple_top_level_results_are_unioned():
    result = evaluate_with_modules(
        "cube(1); translate([5, 0, 0]) cube(1);",
        [CubeModule(), TranslateModule()],
    )
    assert result.volume() == pytest.approx(2.0)


def test_unknown_module_raises():
    with pytest.raises(ValueError, match="Unknown module: 'sphare'"):
        evaluate_with_modules("sphare(1);", [RecordingModule("probe")])


def test_missing_required_parameter_raises():
    probe = RecordingModule("probe")
    with pytest.raises(ValueError, match="Undefined parameter"):
        evaluate_with_modules("probe();", [probe])


def test_default_parameter_supplied_when_omitted():
    class WithDefault(RecordingModule):
        def __init__(self):
            super().__init__("with_default", required=())
            self._parameters = self.make_parameters(optional={"value": NumberLiteral(42.0)})

    module = WithDefault()
    evaluate_with_modules("with_default();", [module])
    assert module.calls == [{"value": 42.0}]


def test_children_are_not_evaluated_unless_module_asks():
    # The core of the new contract: a module that never calls
    # ctx.evaluate_children() leaves its subtree unevaluated.
    class LazyModule(BuiltinModule):
        def instantiate(self, ctx: EvalContext) -> Manifold:
            return Manifold.cube([2.0, 2.0, 2.0])

        @property
        def name(self) -> str:
            return "lazy"

        @property
        def parameters(self) -> Mapping[str, Assignment]:
            return {}

    child = RecordingModule("probe")
    result = evaluate_with_modules("lazy() probe(1);", [LazyModule(), child])
    assert child.calls == []
    assert result.volume() == pytest.approx(8.0)


def test_for_loop_implemented_as_ordinary_builtin():
    # The architecture goal made concrete: `for` needs no evaluator special
    # case — it re-instantiates its body per value with a fresh binding.
    probe = RecordingModule("probe")
    result = evaluate_with_modules(
        "for(values = [10, 20, 30]) probe(i);",
        [ForLoopModule(), probe],
    )
    assert probe.calls == [{"value": 10.0}, {"value": 20.0}, {"value": 30.0}]
    # Three coincident unit cubes union to one
    assert result.volume() == pytest.approx(1.0)


def test_for_loop_body_sees_surrounding_scope():
    # The loop variable shadows, but outer bindings remain visible.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "outer = 5; for(values = [1]) probe(outer);",
        [ForLoopModule(), probe],
    )
    assert probe.calls == [{"value": 5.0}]

# --- user-defined modules ---


def test_user_module_call_evaluates_body():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "module Foo() { probe(1); } Foo();",
        [probe],
    )
    assert probe.calls == [{"value": 1.0}]


def test_user_module_parameters_bind_to_body():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "module Foo(a, b=2) { probe(a); probe(b); } Foo(10);",
        [probe],
    )
    assert probe.calls == [{"value": 10.0}, {"value": 2.0}]


def test_user_module_body_sees_surrounding_scope():
    # A module defined at top level sees top-level variables lexically.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "width = 5; module Foo() { probe(width); } Foo();",
        [probe],
    )
    assert probe.calls == [{"value": 5.0}]


def test_user_module_does_not_see_call_site_plain_variables():
    # Ordinary variables are lexical: a binding at the call site (in a
    # different scope than the definition) is not visible inside the body.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "module Foo() { probe(x); } { x = 99; Foo(); }",
        [probe],
    )
    assert probe.calls == [{"value": None}]


def test_user_module_does_see_call_site_special_variables():
    # Special variables are dynamic: a binding at the call site (in a
    # different scope than the definition) is visible inside the body.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "$x = 100; module Foo() { probe($x); } { $x = 99; Foo(); }",
        [probe],
    )
    assert probe.calls == [{"value": 99}]

def test_user_module_defined_inside_block_is_scoped_to_block():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "{ module Bar() { probe(1); } Bar(); }",
        [probe],
    )
    assert probe.calls == [{"value": 1.0}]
    # Bar is not visible outside the block.
    with pytest.raises(ValueError, match="Unknown module: 'Bar'"):
        evaluate_with_modules(
            "{ module Bar() { probe(1); } } Bar();",
            [probe],
        )


def test_user_module_body_uses_geometry_modules():
    # A user module that wraps a built-in geometry module produces geometry.
    result = evaluate_with_modules(
        "module Box() { cube([1,1,1]); } Box();",
        [CubeModule(), TranslateModule()],
    )
    assert result.volume() == pytest.approx(1.0)


def test_user_module_children_module_works():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "module Bar() { children(0); } Bar() { probe(50); }",
        [probe],
    )
    assert probe.calls == [{"value": 50}]


def test_user_module_children_module_ignores_missing_child():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "module Bar() { children(10); } Bar() { probe(50); }",
        [probe],
    )
    assert probe.calls == []

def test_user_module_children_module_picks_proper_child():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "module Bar() { children(1); } Bar() { probe(10); probe(20); probe(30); }",
        [probe],
    )
    assert probe.calls == [{"value": 20}]