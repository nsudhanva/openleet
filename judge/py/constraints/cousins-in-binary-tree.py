"""Cousins in Binary Tree: a level-order tree with unique values, and two values x, y in it."""


def check(root: list, x: int, y: int) -> None:
    vals = [v for v in root if v is not None]
    assert root and root[0] is not None, "the tree has a root"
    assert 2 <= len(vals) <= 100, "the number of nodes is in the range [2, 100]"
    assert all(1 <= v <= 100 for v in vals), "1 <= Node.val <= 100"
    assert len(set(vals)) == len(vals), "each node has a unique value"
    assert x != y, "x != y"
    assert x in vals and y in vals, "x and y exist in the tree"
