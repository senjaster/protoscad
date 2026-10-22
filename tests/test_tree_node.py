from __future__ import annotations

from manifold_learn.ast.expression import BinaryOp, NumberLiteral, Variable, Assignment
from manifold_learn.ast.tree_node import TreeNode


def make_node(module: str = "root") -> TreeNode:
    return TreeNode(module=module, positional_args=[], named_args={})


def test_construction_defaults():
    node = make_node("cube")
    assert node.module == "cube"
    assert node.positional_args == []
    assert node.named_args == {}
    assert node.parent is None
    assert node.children == []
    assert node._variables == {}
    assert node._modules == {}


def test_add_child_sets_parent():
    parent = make_node()
    child = make_node("cube")
    parent.add_child(child)
    assert parent.children == [child]
    assert child.parent is parent


def test_children_sequence_is_the_raw_list():
    # The `children` property returns the underlying mutable list directly,
    # despite the comment claiming it "conceals the fact it is mutable".
    parent = make_node()
    child = make_node()
    parent.add_child(child)
    assert parent.children is parent._children
    # Mutating the returned sequence mutates the node (no copy is returned)
    parent.children.append(make_node())
    assert len(parent.children) == 2


def test_remove_child_clears_parent():
    parent = make_node()
    child = make_node()
    parent.add_child(child)
    parent.remove_child(child)
    assert parent.children == []
    assert child.parent is None


def test_assign_and_eval_variable_local():
    node = make_node()
    node.assign_variable(Assignment("x", NumberLiteral(5.0)))
    assert node.eval_variable("x") == 5.0


def test_eval_variable_falls_back_to_parent():
    parent = make_node()
    parent.assign_variable(Assignment("x", NumberLiteral(10.0)))
    child = make_node()
    parent.add_child(child)
    assert child.eval_variable("x") == 10.0


def test_eval_variable_missing_returns_none():
    assert make_node().eval_variable("nope") is None


def test_child_variable_shadows_parent():
    parent = make_node()
    parent.assign_variable(Assignment("x", NumberLiteral(10.0)))
    child = make_node()
    parent.add_child(child)
    child.assign_variable(Assignment("x", NumberLiteral(99.0)))
    assert child.eval_variable("x") == 99.0
    # Parent scope unaffected
    assert parent.eval_variable("x") == 10.0


def test_shadowing_references_parent_scope_on_rhs():
    # OpenSCAD declarative semantics: a redefinition in an inner scope may
    # reference the same-named variable from the parent scope on its RHS.
    # The definition must not see itself (no self-reference).
    parent = make_node()
    parent.assign_variable(Assignment("x", NumberLiteral(100.0)))
    child = make_node()
    parent.add_child(child)
    # x = x / 2 in the child scope: RHS x resolves to the parent's x (100)
    child.assign_variable(Assignment("x", BinaryOp("/", Variable("x"), NumberLiteral(2.0))))
    assert child.eval_variable("x") == 50.0
    # Parent scope keeps its own value
    assert parent.eval_variable("x") == 100.0


def test_set_and_get_module_local():
    node = make_node()
    node.set_module("cube", object())
    assert node.get_module("cube") is not None


def test_get_module_falls_back_to_parent():
    parent = make_node()
    marker = object()
    parent.set_module("cube", marker)
    child = make_node()
    parent.add_child(child)
    assert child.get_module("cube") is marker


def test_get_module_missing_returns_none():
    assert make_node().get_module("nope") is None