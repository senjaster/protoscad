from __future__ import annotations

from manifold_learn.ast.expression import Assignment, NumberLiteral
from manifold_learn.ast.tree_node import TreeNode


def make_node(module: str = "root") -> TreeNode:
    return TreeNode(module=module)


def test_construction_defaults():
    node = make_node("cube")
    assert node.module == "cube"
    assert node.positional_args == []
    assert node.named_args == {}
    assert node.parent is None
    assert node.children == []
    assert node.variables == {}


def test_tree_is_pure_data():
    # The node no longer resolves anything: scope behaviour lives in
    # Environment, and the tree only records what the source said.
    node = make_node()
    node.assign_variable(Assignment("x", NumberLiteral(5.0)))
    assert node.variables == {"x": Assignment("x", NumberLiteral(5.0))}


def test_add_child_sets_parent():
    parent = make_node()
    child = make_node("cube")
    parent.add_child(child)
    assert parent.children == [child]
    assert child.parent is parent


def test_last_assignment_wins_as_data():
    node = make_node()
    node.assign_variable(Assignment("x", NumberLiteral(1.0)))
    node.assign_variable(Assignment("x", NumberLiteral(2.0)))
    assert node.variables["x"] == Assignment("x", NumberLiteral(2.0))
