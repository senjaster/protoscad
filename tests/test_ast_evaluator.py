from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest
from antlr4 import CommonTokenStream, InputStream
from manifold3d import Manifold

from protoscad.builtins.cube import CubeModule
from protoscad.builtins.loops import ForModule, IntersectionForModule
from protoscad.builtins.sphere import SphereModule
from protoscad.builtins.translate import TranslateModule
from protoscad.diagnostics import ProtoSCADError
from protoscad.grammar.OpenSCADLexer import OpenSCADLexer
from protoscad.grammar.OpenSCADParser import OpenSCADParser
from protoscad.runtime.evaluator import evaluate
from protoscad.runtime.invocation import Invocation
from protoscad.runtime.module_definition import BuiltinModule
from protoscad.runtime.resolver import OpenScadResolver
from protoscad.tree.expression import Assignment, NumberLiteral
from protoscad.tree.statement import ModuleCallStatement
from protoscad.tree.visitor import AstOpenSCADVisitor

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
        self.calls.append(dict(ctx.arg_values))
        return MARKER_GEOMETRY

    @property
    def name(self) -> str:
        return self._name

    @property
    def parameters(self) -> Mapping[str, Assignment]:
        return self._parameters


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
    with pytest.raises(ProtoSCADError, match="Unknown variable 'zz'"):
        evaluate_with_modules("q = zz;", [RecordingModule("probe")])


def test_declarative_cycle_errors_when_used():
    # The final definitions x = y+1 and y = x form a cycle; forcing it
    # raises with the forcing path.
    probe = RecordingModule("probe")
    with pytest.raises(ProtoSCADError, match="Circular variable dependency: x -> y -> x"):
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
            self.sizes.append(ctx.arg_values["size"])
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
    with pytest.raises(ProtoSCADError, match="'x' .* before its first assignment"):
        evaluate_with_modules("y = x; x = 10; probe(y);", [probe], OpenScadResolver())


def test_openscad_unknown_variable_in_binding_raises():
    # Bindings are evaluated eagerly at scope setup, so even an unused
    # binding with an unknown name fails (OpenSCAD warns; we raise).
    with pytest.raises(ProtoSCADError, match="Unknown variable 'zz'"):
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
    with pytest.raises(ProtoSCADError, match="Circular variable dependency"):
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
    with pytest.raises(ProtoSCADError, match="Unknown module: 'sphare'"):
        evaluate_with_modules("sphare(1);", [RecordingModule("probe")])


def test_missing_required_parameter_raises():
    probe = RecordingModule("probe")
    with pytest.raises(ProtoSCADError, match="Missing required parameter"):
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


## =========================================================================
#  for() / intersection_for()


def test_for_loop_iterates_vector():
    probe = RecordingModule("probe")
    result = evaluate_with_modules("for(i = [10, 20, 30]) probe(i);", [ForModule(), probe])
    assert probe.calls == [{"value": 10.0}, {"value": 20.0}, {"value": 30.0}]
    # Three coincident unit cubes union to one
    assert result.volume() == pytest.approx(1.0)


def test_for_loop_iterates_range_with_step():
    probe = RecordingModule("probe")
    evaluate_with_modules("for(i = [0:2:6]) probe(i);", [ForModule(), probe])
    assert probe.calls == [{"value": 0.0}, {"value": 2.0}, {"value": 4.0}, {"value": 6.0}]


def test_for_loop_single_value_iterates_once():
    probe = RecordingModule("probe")
    evaluate_with_modules("for(i = 5) probe(i);", [ForModule(), probe])
    assert probe.calls == [{"value": 5.0}]


def test_for_loop_empty_iteration_set_evaluates_nothing():
    probe = RecordingModule("probe")
    evaluate_with_modules("for(i = []) probe(1);", [ForModule(), probe])
    assert probe.calls == []


def test_for_loop_nested_variables_iterate_cartesian_product():
    probe = RecordingModule("probe")
    probe2 = RecordingModule("probe2")
    evaluate_with_modules(
        "for(i = [0, 1], j = [5, 6]) { probe(i); probe2(j); }",
        [ForModule(), probe, probe2],
    )
    # The leftmost variable is the outermost loop.
    assert probe.calls == [{"value": 0.0}, {"value": 0.0}, {"value": 1.0}, {"value": 1.0}]
    assert probe2.calls == [{"value": 5.0}, {"value": 6.0}, {"value": 5.0}, {"value": 6.0}]


def test_for_loop_body_binding_uses_current_iteration_value():
    # The canonical OpenSCAD idiom: a binding in the body must see the
    # current iteration's value, not the first or last one.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "for(i = [0, 1]) { angle = i * 90; probe(angle); }",
        [ForModule(), probe],
    )
    assert probe.calls == [{"value": 0.0}, {"value": 90.0}]


def test_for_loop_body_sees_surrounding_scope():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "outer = 5; for(i = [1]) probe(outer);",
        [ForModule(), probe],
    )
    assert probe.calls == [{"value": 5.0}]


def test_for_loop_variable_shadows_outer_binding():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "i = 99; for(i = [1]) probe(i);",
        [ForModule(), probe],
    )
    assert probe.calls == [{"value": 1.0}]


def test_for_loop_special_variable_binding():
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "for($i = [7, 8]) probe($i);",
        [ForModule(), probe],
    )
    assert probe.calls == [{"value": 7.0}, {"value": 8.0}]


def test_for_loop_variable_is_lexical_inside_user_modules():
    # A module called from the body resolves names in its definition scope;
    # the loop variable exists only in the body's own scope.
    probe = RecordingModule("probe")
    evaluate_with_modules(
        "i = 99; module Foo() { probe(i); } for(i = [1]) Foo();",
        [ForModule(), probe],
    )
    assert probe.calls == [{"value": 99.0}]


def test_for_loop_unions_geometry():
    result = evaluate_with_modules(
        "for(i = [0, 10]) translate([i, 0, 0]) cube(2);",
        [CubeModule(), ForModule(), TranslateModule()],
    )
    assert result.volume() == pytest.approx(16.0)


def test_intersection_for_intersects_iterations():
    result = evaluate_with_modules(
        "intersection_for(i = [0, 1]) translate([i, 0, 0]) cube(2);",
        [CubeModule(), IntersectionForModule(), TranslateModule()],
    )
    # Two cubes offset by one along x share a 1x2x2 slab.
    assert result.volume() == pytest.approx(4.0)


def test_for_loop_rejects_positional_arguments():
    probe = RecordingModule("probe")
    with pytest.raises(ProtoSCADError, match="loop bindings"):
        evaluate_with_modules("for([0:3]) probe(1);", [ForModule(), probe])


def test_for_loop_without_bindings_raises():
    probe = RecordingModule("probe")
    with pytest.raises(ProtoSCADError, match="at least one"):
        evaluate_with_modules("for() probe(1);", [ForModule(), probe])


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
    with pytest.raises(ProtoSCADError, match="Unknown module: 'Bar'"):
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
    with pytest.raises(ProtoSCADError, match="Missing required parameter"):
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


def test_geometry_builtin_consumes_special_variable_argument():
    # SphereModule reads $fn from the call environment: more fragments
    # refine the mesh toward the ideal 4/3*pi, always from below —
    # a faceted sphere under-approximates.
    coarse = evaluate_with_modules("sphere($fn = 4);", [SphereModule()])
    fine = evaluate_with_modules("sphere($fn = 12);", [SphereModule()])
    assert 0 < coarse.volume() < fine.volume() < 4.18879


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
    with pytest.raises(ProtoSCADError, match="Unknown parameter 'bogus'"):
        evaluate_with_modules("cube(size = 1, bogus = 2);", [CubeModule()])


def test_too_many_positional_arguments_raise():
    with pytest.raises(ProtoSCADError, match="positional"):
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
    # The string argument now evaluates to its unquoted content (it used to
    # be the raw source text while strings were a stub).
    assert echo.calls == [{"value": "bbb"}]


def test_children_module_invocation_is_single_child():
    # QUIRKS.md: a module invocation union(){...} is a single child, so
    # children(1) yields the whole union (which evaluates to both echoes).
    echo = RecordingModule("echo")
    evaluate_with_modules(
        'module my_mod() { children(1); } my_mod() { echo("aaa"); union() { echo("bbb"); echo("ccc"); } }',
        [echo],
    )
    assert echo.calls == [{"value": "bbb"}, {"value": "ccc"}]


## =========================================================================
#  Expressions end-to-end: constants, builtin functions, ternary, strings


def test_builtin_constant_pi_resolves_everywhere():
    probe = RecordingModule("probe")
    evaluate_with_modules("probe(2*PI);", [probe])
    assert probe.calls[0]["value"] == pytest.approx(6.283185307179586)


def test_local_assignment_shadows_pi():
    probe = RecordingModule("probe")
    evaluate_with_modules("PI = 3; probe(PI);", [probe])
    assert probe.calls[0]["value"] == 3.0


def test_builtin_function_call_in_argument():
    probe = RecordingModule("probe")
    evaluate_with_modules("probe(floor(3.7) + max(1, 5));", [probe])
    assert probe.calls[0]["value"] == 8.0


def test_ternary_and_logical_operators_end_to_end():
    probe = RecordingModule("probe")
    evaluate_with_modules('x = 4; probe(x > 3 && x < 5 ? "big" : "small");', [probe])
    assert probe.calls[0]["value"] == "big"


def test_index_and_range_in_source():
    probe = RecordingModule("probe")
    evaluate_with_modules("v = [10, 20, 30]; probe(v[1]);", [probe])
    assert probe.calls[0]["value"] == 20.0


def test_type_error_carries_span_from_source():
    probe = RecordingModule("probe")
    with pytest.raises(ProtoSCADError) as excinfo:
        evaluate_with_modules('s = "a"; probe(s + 1);', [probe])
    diagnostic = excinfo.value.diagnostic
    assert diagnostic.code.value == "type-error"
    assert diagnostic.span is not None
    assert diagnostic.span.start_line == 1
