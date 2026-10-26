from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest
from antlr4 import CommonTokenStream, InputStream
from manifold3d import Manifold

from manifold_learn.builtins.cube import CubeModule
from manifold_learn.builtins.sphere import SphereModule
from manifold_learn.builtins.translate import TranslateModule
from manifold_learn.grammar.OpenSCADLexer import OpenSCADLexer
from manifold_learn.grammar.OpenSCADParser import OpenSCADParser
from manifold_learn.runtime.evaluator import evaluate
from manifold_learn.runtime.invocation import Invocation
from manifold_learn.runtime.module_definition import BuiltinModule
from manifold_learn.runtime.resolver import OpenScadResolver
from manifold_learn.tree.expression import Assignment, NumberLiteral
from manifold_learn.tree.statement import ModuleCallStatement
from manifold_learn.tree.visitor import AstOpenSCADVisitor

MARKER_GEOMETRY = Manifold.cube([1.0, 1.0, 1.0])


def parse_scad(source: str) -> ModuleCallStatement:
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


class RecordingModule(BuiltinModule):
    """Test double: records evaluated args, returns a marker geometry."""

    def __init__(self, name: str, required=("value",)):
        self._name = name
        self._parameters = self.make_parameters(required=required)
        self.calls: list[dict[str, Any]] = []

    def instantiate(self, ctx: Invocation) -> Manifold:
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

    def instantiate(self, ctx: Invocation) -> list[Manifold]:
        results = []
        for value in ctx.args["values"]:
            env = ctx.child_env.extend_variables({"i": Assignment("i", NumberLiteral(value))})
            for statement in ctx.children:
                results.append(ctx.evaluate(statement, env))
        return results

    @property
    def name(self) -> str:
        return "for"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self.make_parameters(required=("values",))


class SpecialVarProbeModule(BuiltinModule):
    """Records the `$fn` value visible at the point where this module is
    instantiated (i.e. what a geometry builtin would consume there)."""

    def __init__(self):
        self.calls: list[dict[str, Any]] = []

    def instantiate(self, ctx: Invocation) -> Manifold:
        self.calls.append({"$fn": ctx.child_env.lookup_variable("$fn")})
        return MARKER_GEOMETRY

    @property
    def name(self) -> str:
        return "sv_probe"

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return {}


def evaluate_with_modules(source: str, modules, resolver=None):
    scope = parse_scad(source)
    return evaluate(scope, modules, resolver=resolver)


## =========================================================================
#  Variable bindings (DeclarativeResolver, the default policy)


def test_top_level_assignment_visible_to_module_args():
    probe = RecordingModule("probe")
    evaluate_with_modules("width = 10; probe(width);", [probe])
    assert probe.calls == [{"value": 10.0}]


def test_last_assignment_wins_for_whole_scope():
    probe = RecordingModule("probe")
    evaluate_with_modules("width = 10; width = 100; probe(width);", [probe])
    assert probe.calls == [{"value": 100.0}]


def test_declarative_binding_sees_final_value():
    # Letrec: a scope is a set of simultaneous definitions, so y sees the
    # final x (the same outcome OpenSCAD gives for this program).
    probe = RecordingModule("probe")
    evaluate_with_modules("x = 1; y = x; x = 10; probe(y); probe(x);", [probe])
    assert probe.calls == [{"value": 10.0}, {"value": 10.0}]


def test_declarative_self_reference_uses_parent():
    # The shadowing idiom survives: inside a real scope, `width = width/2`
    # reads the enclosing width on its right-hand side.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "width = 100; union() { width = width / 2; probe(width); } probe(width);",
        [probe],
    )
    assert probe.calls == [{"value": 50.0}, {"value": 100.0}]


def test_declarative_local_shadows_parent_whole_scope():
    # A name bound anywhere in the scope is local to the whole scope, so
    # `y = m` reads the scope's own final m — not the parent's m=5. (Real
    # OpenSCAD gives 5 here; this is the deliberate declarative fix.)
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "m = 5; union() { y = m; m = 1; probe(y); } probe(m);",
        [probe],
    )
    assert probe.calls == [{"value": 1.0}, {"value": 5.0}]


def test_declarative_shadowed_binding_never_evaluates():
    # Redefinition replaces the definition: the earlier `q = zz` never
    # exists, so the unknown zz is not an error (same as OpenSCAD mode).
    probe = RecordingModule("probe")
    evaluate_with_modules("q = zz; q = 7; probe(q);", [probe])
    assert probe.calls == [{"value": 7.0}]


def test_declarative_unknown_variable_in_binding_raises():
    # Unknown names in bindings are rejected at scope setup, even when the
    # binding is never used.
    with pytest.raises(ValueError, match="Unknown variable 'zz'"):
        evaluate_with_modules("q = zz;", [RecordingModule("probe")])


def test_declarative_cycle_errors_when_used():
    # The final definitions x = y+1 and y = x form a cycle; forcing it
    # raises with the forcing path.
    probe = RecordingModule("probe")
    with pytest.raises(ValueError, match="Circular variable dependency: x -> y -> x"):
        evaluate_with_modules("x = 1; y = x; x = y + 1; probe(x);", [probe])


def test_declarative_unused_cycle_is_tolerated():
    # Bindings are forced on first use: an unguarded cycle that nothing
    # reads is dead code, not an error (as in Haskell or Nix).
    probe = RecordingModule("probe")
    evaluate_with_modules("x = y; y = x; probe(1);", [probe])
    assert probe.calls == [{"value": 1.0}]


def test_declarative_forward_reference_in_scope():
    # A module call may precede the variable binding and module definition
    # it depends on within the same scope: calls see the scope's map
    # regardless of source order.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "my_module(var1); module my_module(x) { probe(x); } var1 = 10;",
        [probe],
    )
    assert probe.calls == [{"value": 10.0}]


def test_call_argument_sees_final_value_of_redefined_variable():
    # Verified against real OpenSCAD: `cube_size=5; cube(cube_size);
    # cube_size=20;` produces a 20-unit cube — call arguments run after
    # the scope's bindings, so they see final values in both modes.
    class SizeProbe(BuiltinModule):
        def __init__(self):
            self.sizes: list[Any] = []

        def instantiate(self, ctx: Invocation) -> Manifold:
            self.sizes.append(ctx.args["size"])
            return MARKER_GEOMETRY

        @property
        def name(self) -> str:
            return "size_probe"

        @property
        def parameters(self) -> Mapping[str, Assignment]:
            return self.make_parameters(required=("size",))

    probe = SizeProbe()
    evaluate_with_modules("s = 5; size_probe(s); s = 20;", [probe])
    assert probe.sizes == [20.0]


## =========================================================================
#  Variable bindings (OpenScadResolver: OpenSCAD-verified quirks)


def test_openscad_binding_sees_final_scope_values():
    # Verified against real OpenSCAD: `x=1; y=x; x=3;` yields y=3 — a
    # binding sees the FINAL value of variables first defined before it.
    probe = RecordingModule("probe")
    evaluate_with_modules("width = 10; depth = width * 2; width = 100; probe(depth);", [probe], OpenScadResolver())
    assert probe.calls == [{"value": 200.0}]


def test_openscad_use_before_first_definition_raises():
    # OpenSCAD treats `y = x; x = 10;` as unknown x (warning + undef); we
    # raise the same case as an error instead of passing None around.
    probe = RecordingModule("probe")
    with pytest.raises(ValueError, match="'x' .* before its first assignment"):
        evaluate_with_modules("y = x; x = 10; probe(y);", [probe], OpenScadResolver())


def test_openscad_unknown_variable_in_binding_raises():
    # Bindings are evaluated eagerly at scope setup, so even an unused
    # binding with an unknown name fails (OpenSCAD warns; we raise).
    with pytest.raises(ValueError, match="Unknown variable 'zz'"):
        evaluate_with_modules("q = zz;", [RecordingModule("probe")], OpenScadResolver())


def test_openscad_shadowed_binding_is_never_evaluated():
    # Only the last binding of a name runs: the earlier `q = zz` (unknown
    # zz) never evaluates, matching OpenSCAD (verified: no warning).
    probe = RecordingModule("probe")
    evaluate_with_modules("q = zz; q = 7; probe(q);", [probe], OpenScadResolver())
    assert probe.calls == [{"value": 7.0}]


def test_openscad_later_first_definition_falls_through_to_parent():
    # Inside the union, `y = m` precedes m's first local definition, so m
    # resolves in the parent scope (verified: OpenSCAD yields y=5 and the
    # outer m stays 5).
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "m = 5; union() { y = m; m = 1; probe(y); } probe(m);",
        [probe],
        OpenScadResolver(),
    )
    assert probe.calls == [{"value": 5.0}, {"value": 5.0}]


def test_openscad_circular_binding_dependency_raises():
    # OpenSCAD degrades `x=1; y=x; x=y+1;` to undef everywhere; we raise.
    with pytest.raises(ValueError, match="Circular variable dependency"):
        evaluate_with_modules("x = 1; y = x; x = y + 1;", [RecordingModule("probe")], OpenScadResolver())


## =========================================================================
#  let


def test_let_binding_visible_to_children():
    probe = RecordingModule("probe")
    result = evaluate_with_modules("let(offset = 4) { probe(offset); }", [probe])
    assert probe.calls == [{"value": 4.0}]
    assert result.volume() == pytest.approx(1.0)


def test_let_binding_not_visible_outside():
    probe = RecordingModule("probe")
    evaluate_with_modules("let(offset = 4) { probe(1); } probe(offset);", [probe])
    assert probe.calls == [{"value": 1.0}, {"value": None}]


def test_sibling_does_not_see_let_binding():
    probe = RecordingModule("probe")
    evaluate_with_modules("let(x = 1) probe(1); probe(x);", [probe])
    assert probe.calls == [{"value": 1.0}, {"value": None}]


## =========================================================================
#  Blocks are transparent


def test_bare_block_variable_leaks_to_enclosing_scope():
    # QUIRKS.md: a bare block is transparent (no new scope), so `local`
    # binds in the top-level scope and is visible to the second probe.
    probe = RecordingModule("probe")
    evaluate_with_modules("{ local = 7; probe(local); } probe(local);", [probe])
    assert probe.calls == [{"value": 7.0}, {"value": 7.0}]


def test_shadowing_references_parent_on_rhs_across_real_scope():
    # A module invocation (union) is a real scope: inside it, `width = width/2`
    # references the enclosing top-level width (self-reference excluded).
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "width = 100; union() { width = width / 2; probe(width); } probe(width);",
        [probe],
    )
    assert probe.calls == [{"value": 50.0}, {"value": 100.0}]


## =========================================================================
#  Multiple results / errors


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


## =========================================================================
#  Lazy children contract


def test_children_are_not_evaluated_unless_module_asks():
    class LazyModule(BuiltinModule):
        def instantiate(self, ctx: Invocation) -> Manifold:
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
    probe = RecordingModule("probe")
    result = evaluate_with_modules(
        "for(values = [10, 20, 30]) probe(i);",
        [ForLoopModule(), probe],
    )
    assert probe.calls == [{"value": 10.0}, {"value": 20.0}, {"value": 30.0}]
    # Three coincident unit cubes union to one
    assert result.volume() == pytest.approx(1.0)


def test_for_loop_body_sees_surrounding_scope():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "outer = 5; for(values = [1]) probe(outer);",
        [ForLoopModule(), probe],
    )
    assert probe.calls == [{"value": 5.0}]


## =========================================================================
#  User-defined modules


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
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "width = 5; module Foo() { probe(width); } Foo();",
        [probe],
    )
    assert probe.calls == [{"value": 5.0}]


def test_user_module_does_not_see_call_site_plain_variables():
    # Ordinary variables are lexical: a binding at the call site (inside a
    # real module invocation, a different scope than the definition) is not
    # visible inside the body.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "module Foo() { probe(x); } union() { x = 99; Foo(); }",
        [probe],
    )
    assert probe.calls == [{"value": None}]


def test_user_module_does_see_call_site_special_variables():
    # Special variables are dynamic: a binding at the call site (in a
    # different scope than the definition) is visible inside the body.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "$x = 100; module Foo() { probe($x); } union() { $x = 99; Foo(); }",
        [probe],
    )
    assert probe.calls == [{"value": 99}]


def test_user_module_defined_inside_real_scope_is_scoped_to_it():
    # A module defined inside a module invocation (a real scope) is not
    # visible outside it.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "union() { module Bar() { probe(1); } Bar(); }",
        [probe],
    )
    assert probe.calls == [{"value": 1.0}]
    with pytest.raises(ValueError, match="Unknown module: 'Bar'"):
        evaluate_with_modules(
            "union() { module Bar() { probe(1); } } Bar();",
            [probe],
        )


def test_user_module_body_uses_geometry_modules():
    result = evaluate_with_modules(
        "module Box() { cube([1,1,1]); } Box();",
        [CubeModule(), TranslateModule()],
    )
    assert result.volume() == pytest.approx(1.0)


def test_user_module_default_resolves_in_definition_scope():
    # A default expression follows the definition-site binding (width = 5),
    # not the call-site shadow (width = 100 inside the union).
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "width = 5; module Foo(b = width * 2) { probe(b); } union() { width = 100; Foo(); }",
        [probe],
    )
    assert probe.calls == [{"value": 10.0}]


def test_user_module_explicit_arg_resolves_in_call_scope():
    # Explicit arguments are caller-scoped: width inside the union is 100.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "width = 5; module Foo(b) { probe(b); } union() { width = 100; Foo(width); }",
        [probe],
    )
    assert probe.calls == [{"value": 100.0}]


def test_user_module_missing_required_parameter_raises():
    probe = RecordingModule("probe")
    with pytest.raises(ValueError, match="Undefined parameter"):
        evaluate_with_modules("module Foo(a) { probe(a); } Foo();", [probe])


## =========================================================================
# Special-variable arguments (`module_name(..., $fn = 36)`)


def test_special_variable_argument_scopes_to_subtree():
    # `$fn = 36` as an argument binds the special variable for the subtree
    # of the call only — not for siblings after it.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "union($fn = 36) probe($fn); probe($fn);",
        [probe],
    )
    assert probe.calls == [{"value": 36.0}, {"value": None}]


def test_special_variable_argument_visible_in_user_module_body():
    # The overlay reaches user module bodies through the dynamic chain.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "module Foo() { probe($fn); } Foo($fn = 36);",
        [probe],
    )
    assert probe.calls == [{"value": 36.0}]


def test_builtin_reads_special_variable_argument():
    probe = SpecialVarProbeModule()
    evaluate_with_modules("sv_probe($fn = 36); sv_probe();", [probe])
    assert probe.calls == [{"$fn": 36.0}, {"$fn": None}]


def test_geometry_builtin_accepts_special_variable_argument():
    # $fn is routed into the subtree environment; SphereModule does not
    # consume it yet, so this only asserts the call evaluates to a proper
    # solid (a faceted unit sphere has volume below the ideal 4/3*pi).
    result = evaluate_with_modules("sphere($fn = 12);", [SphereModule()])
    assert 0 < result.volume() < 4.18879


def test_special_variable_argument_visible_to_sibling_args():
    # The `$`-overlay wraps the call itself (call_env), so other argument
    # expressions of the same call resolve through it.
    probe = RecordingModule("probe")
    evaluate_with_modules("probe($fn = 36, value = $fn);", [probe])
    assert probe.calls == [{"value": 36.0}]


def test_module_can_inject_special_variable_into_children():
    # A module can extend child_env before dispatching a child: the child
    # sees the injected `$`-variable, but nothing outside the module does.
    class FnInjector(BuiltinModule):
        def instantiate(self, ctx: Invocation) -> list[Manifold]:
            env = ctx.child_env.extend_variables({"$fn": Assignment("$fn", NumberLiteral(8.0))})
            return [ctx.evaluate(statement, env) for statement in ctx.children]

        @property
        def name(self) -> str:
            return "fn_injector"

        @property
        def parameters(self) -> Mapping[str, Assignment]:
            return {}

    probe = SpecialVarProbeModule()
    evaluate_with_modules("fn_injector() sv_probe(); sv_probe();", [FnInjector(), probe])
    assert probe.calls == [{"$fn": 8.0}, {"$fn": None}]


## =========================================================================
# Argument validation


def test_unknown_named_argument_raises():
    with pytest.raises(ValueError, match="Unknown parameter 'bogus'"):
        evaluate_with_modules("cube(size = 1, bogus = 2);", [CubeModule()])


def test_too_many_positional_arguments_raise():
    with pytest.raises(ValueError, match="positional"):
        evaluate_with_modules("cube(1, 2, 3);", [CubeModule()])


## =========================================================================
# Divergence from OpenSCAD: `$`-arguments on builtin calls
#
# Verified against real OpenSCAD:
#   union($fn=360) sphere(1);                          -> COARSE sphere
#   module mysphere() {...} mysphere($fn=360) sphere(1); -> both spheres fine
#   let($fn=360) sphere(1);                            -> fine sphere
#
# In OpenSCAD, `$`-arguments extend only the context the called module
# itself runs in (that is why the leaf idiom `sphere($fn=100)` works); a
# builtin's children evaluate in the calling scope, untouched. We extend
# the whole subtree scope for every call, builtin or user — simpler and
# uniform, at the cost of the divergence pinned below.
# See docs/QUIRKS.md.


def test_divergence_builtin_special_args_reach_children():
    # OpenSCAD renders `union($fn=360) sphere(1);` with a COARSE sphere:
    # the child never sees the special argument on the builtin call.
    # We deliberately let it through.
    probe = SpecialVarProbeModule()
    evaluate_with_modules("union($fn = 360) sv_probe();", [probe])
    assert probe.calls == [{"$fn": 360.0}]


def test_user_module_special_args_match_openscad():
    # OpenSCAD renders both the body sphere and the children() sphere
    # fine-grained for `mysphere($fn=360) sphere(1);` — we match: the
    # special argument is visible in the body and in children() alike.
    probe = SpecialVarProbeModule()
    evaluate_with_modules(
        "module mysphere() { sv_probe(); children(0); } mysphere($fn = 360) sv_probe();",
        [probe],
    )
    assert probe.calls == [{"$fn": 360.0}, {"$fn": 360.0}]


def test_let_special_args_match_openscad():
    # OpenSCAD renders `let($fn=360) sphere(1);` fine-grained — we match.
    probe = SpecialVarProbeModule()
    evaluate_with_modules("let($fn = 360) sv_probe();", [probe])
    assert probe.calls == [{"$fn": 360.0}]


## =========================================================================
#  children()


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


def test_children_bare_block_unwrapped():
    # QUIRKS.md: a bare block is transparent, so children(1) yields `bbb` only.
    echo = RecordingModule("echo")
    evaluate_with_modules(
        'module my_mod() { children(1); } my_mod() { echo("aaa"); { echo("bbb"); echo("ccc"); } }',
        [echo],
    )
    assert echo.calls == [{"value": '"bbb"'}]


def test_children_module_invocation_is_single_child():
    # QUIRKS.md: a module invocation union(){...} is a single child, so
    # children(1) yields the whole union (which evaluates to both echoes).
    echo = RecordingModule("echo")
    evaluate_with_modules(
        'module my_mod() { children(1); } my_mod() { echo("aaa"); union() { echo("bbb"); echo("ccc"); } }',
        [echo],
    )
    assert echo.calls == [{"value": '"bbb"'}, {"value": '"ccc"'}]
