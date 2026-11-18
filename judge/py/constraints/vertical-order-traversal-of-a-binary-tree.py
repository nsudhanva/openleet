"""Vertical Order Traversal of a Binary Tree: a binary tree as a level-order list."""


def check(root: list[int | None]) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has at least one node"
    n = sum(v is not None for v in root)
    assert 1 <= n <= 1000, "number of nodes in [1, 1000]"
    assert all(0 <= v <= 1000 for v in root if v is not None), "0 <= Node.val <= 1000"
