from __future__ import annotations

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from manifold_learn.ast.expression import ArrayLiteral, BinaryOp, NumberLiteral, Variable
from manifold_learn.ast.statement import (
    ModuleCallStatement,
    VariableBindingStatement,
)
from manifold_learn.ast.visitor import AstOpenSCADVisitor
from manifold_learn.grammar.OpenSCADLexer import OpenSCADLexer
from manifold_learn.grammar.OpenSCADParser import OpenSCADParser

# A rich, nested, multi-statement OpenSCAD program exercising chained module
# calls, blocks, let bindings, array literals, variable redefinition and
# scope shadowing.
COMPLEX_SOURCE = """\
// Top-level variables
width = 10;
depth = width * 2;
height = (depth + 5) / 2;

scale([1, 2, 1])
translate([width, depth, height]) {
    box(5, center=true);
    cylinder(r=3, h=height, center=true);
    /* nested block */
    {
        sphere(2);
        translate([0, 0, 1]) cube([1, 1, 1]);
    }
}

let(offset = 4) {
    translate([0, 0, offset]) {
        box(offset);
    }
}

rotate([0, 0, 45]) box(width, center=true);

// Redefine width in the top-level scope: the old definition is discarded
width = 100;

// A block that shadows `width` with a local definition referencing the
// parent-scope value on its right-hand side (valid in OpenSCAD).
{
    width = width / 2;
    box(width);
}
"""


def parse_scad(source: str) -> ModuleCallStatement:
    """Parse source via the OpenSCAD grammar, returning the root scope call."""
    lexer = OpenSCADLexer(InputStream(source))
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    tree = parser.start()
    return AstOpenSCADVisitor().visit(tree)


def parse_scad_with_errors(source: str) -> tuple[ModuleCallStatement, list[str]]:
    """Parse source, returning (root scope call, list of syntax error messages)."""
    errors: list[str] = []

    class Collector(ErrorListener):
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            errors.append(msg)

    lexer = OpenSCADLexer(InputStream(source))
    lexer.removeErrorListeners()
    lexer.addErrorListener(Collector())
    stream = CommonTokenStream(lexer)
    parser = OpenSCADParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(Collector())
    tree = parser.start()
    scope = AstOpenSCADVisitor().visit(tree)
    return scope, errors


def find_modules(scope: ModuleCallStatement, name: str) -> list[ModuleCallStatement]:
    """Return all descendant module-call statements (depth-first) with the given name."""
    found = []
    for statement in scope.children:
        if isinstance(statement, ModuleCallStatement):
            if statement.module == name:
                found.append(statement)
            found.extend(find_modules(statement, name))
    return found


def test_complex_source_satisfies_grammar():
    _, errors = parse_scad_with_errors(COMPLEX_SOURCE)
    assert errors == []


def test_top_level_statements_are_scope_entries():
    scope = parse_scad(COMPLEX_SOURCE)
    # Top-level: three variable bindings, the scale chain, the let, the
    # rotate chain, a redefinition of width, and (from the trailing bare
    # block, which is transparent) a local redefinition and a box call.
    assert [type(s).__name__ for s in scope.children] == [
        "VariableBindingStatement",
        "VariableBindingStatement",
        "VariableBindingStatement",
        "ModuleCallStatement",
        "ModuleCallStatement",
        "ModuleCallStatement",
        "VariableBindingStatement",
        "VariableBindingStatement",
        "ModuleCallStatement",
    ]
    assert [s.module for s in scope.children if isinstance(s, ModuleCallStatement)] == [
        "scale",
        "let",
        "rotate",
        "box",
    ]


def test_chained_scale_translate_box_nesting():
    scope = parse_scad(COMPLEX_SOURCE)
    scale = scope.children[3]
    assert isinstance(scale, ModuleCallStatement)
    assert scale.module == "scale"
    # Array literal builds a list of element expressions
    assert scale.positional_args == [
        ArrayLiteral([NumberLiteral(1.0), NumberLiteral(2.0), NumberLiteral(1.0)])
    ]

    translate = scale.children[0]
    assert isinstance(translate, ModuleCallStatement)
    assert translate.module == "translate"
    # The array literal [width, depth, height] resolves to variables
    assert translate.positional_args == [
        ArrayLiteral([Variable("width"), Variable("depth"), Variable("height")])
    ]

    # translate's body: box, cylinder, and the nested bare block (transparent,
    # so its sphere and translate->cube land directly in translate's children).
    assert [s.module for s in translate.children] == ["box", "cylinder", "sphere", "translate"]

    # box uses a named arg center=true
    box = translate.children[0]
    assert isinstance(box, ModuleCallStatement)
    assert box.module == "box"
    assert box.positional_args == [NumberLiteral(5.0)]
    assert box.named_args == {"center": Variable("true")}

    # cylinder uses named r, h, center
    cylinder = translate.children[1]
    assert isinstance(cylinder, ModuleCallStatement)
    assert cylinder.module == "cylinder"
    assert cylinder.named_args == {
        "r": NumberLiteral(3.0),
        "h": Variable("height"),
        "center": Variable("true"),
    }

    # The nested bare block's sphere
    sphere = translate.children[2]
    assert isinstance(sphere, ModuleCallStatement)
    assert sphere.module == "sphere"
    assert sphere.positional_args == [NumberLiteral(2.0)]

    # The nested translate->cube chain
    inner_translate = translate.children[3]
    assert isinstance(inner_translate, ModuleCallStatement)
    assert inner_translate.module == "translate"
    assert inner_translate.positional_args == [
        ArrayLiteral([NumberLiteral(0.0), NumberLiteral(0.0), NumberLiteral(1.0)])
    ]
    cube = inner_translate.children[0]
    assert isinstance(cube, ModuleCallStatement)
    assert cube.module == "cube"
    assert cube.positional_args == [
        ArrayLiteral([NumberLiteral(1.0), NumberLiteral(1.0), NumberLiteral(1.0)])
    ]


def test_let_binding_becomes_variable_binding_statement():
    scope = parse_scad(COMPLEX_SOURCE)
    let_node = scope.children[4]
    assert isinstance(let_node, ModuleCallStatement)
    assert let_node.module == "let"

    # let's body starts with the binding, then the translate chain
    offset_binding = let_node.children[0]
    assert isinstance(offset_binding, VariableBindingStatement)
    assert offset_binding.name == "offset"
    assert offset_binding.value == NumberLiteral(4.0)

    translate = let_node.children[1]
    assert isinstance(translate, ModuleCallStatement)
    assert translate.module == "translate"
    assert translate.positional_args == [
        ArrayLiteral([NumberLiteral(0.0), NumberLiteral(0.0), Variable("offset")])
    ]
    box = translate.children[0]
    assert isinstance(box, ModuleCallStatement)
    assert box.module == "box"
    # box(offset) references the let-bound variable
    assert box.positional_args == [Variable("offset")]


def test_top_level_assignments_are_variable_binding_statements():
    # Top-level assignments become VariableBindingStatements in the scope;
    # resolution semantics are covered by the evaluator tests.
    scope = parse_scad(COMPLEX_SOURCE)
    # width is redefined to 100 later in the source; both bindings appear as
    # separate statements (last-definition-wins is an evaluator concern).
    assert [
        (s.name, s.value)
        for s in scope.children
        if isinstance(s, VariableBindingStatement) and s.name == "width"
    ] == [
        ("width", NumberLiteral(10.0)),
        ("width", NumberLiteral(100.0)),
        ("width", BinaryOp("/", Variable("width"), NumberLiteral(2.0))),
    ]


def test_rotate_chain_uses_top_level_variable():
    scope = parse_scad(COMPLEX_SOURCE)
    rotate = scope.children[5]
    assert isinstance(rotate, ModuleCallStatement)
    assert rotate.module == "rotate"
    assert rotate.positional_args == [
        ArrayLiteral([NumberLiteral(0.0), NumberLiteral(0.0), NumberLiteral(45.0)])
    ]
    box = rotate.children[0]
    assert isinstance(box, ModuleCallStatement)
    assert box.module == "box"
    # box(width, center=true): width is a Variable reference
    assert box.positional_args == [Variable("width")]
    assert box.named_args == {"center": Variable("true")}


def test_all_module_calls_have_expected_count():
    scope = parse_scad(COMPLEX_SOURCE)
    assert len(find_modules(scope, "cube")) == 1
    # box appears in the scale block, the let block, and the shadowing block
    assert len(find_modules(scope, "box")) == 4
    assert len(find_modules(scope, "sphere")) == 1
    assert len(find_modules(scope, "cylinder")) == 1
    assert len(find_modules(scope, "translate")) == 3


def test_shadowing_block_splices_redefinition_and_box():
    # The trailing bare block is transparent: its statements are spliced into
    # the top-level scope. It contributes a local redefinition of `width`
    # (referencing the parent-scope value on the right-hand side) and a box
    # call. Resolution semantics are covered by the evaluator tests; here we
    # check the tree carries both the redefinition and the reference.
    scope = parse_scad(COMPLEX_SOURCE)
    shadow_redefinition = scope.children[7]
    assert isinstance(shadow_redefinition, VariableBindingStatement)
    assert shadow_redefinition.name == "width"
    assert shadow_redefinition.value == BinaryOp(
        "/",
        Variable("width"),
        NumberLiteral(2.0),
    )
    box = scope.children[8]
    assert isinstance(box, ModuleCallStatement)
    assert box.module == "box"
    assert box.positional_args == [Variable("width")]