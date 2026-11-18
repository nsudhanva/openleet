"""Cousins in Binary Tree II: a binary tree in level-order form."""


def check(root: list) -> None:
    vals = [v for v in root if v is not None]
    assert root and root[0] is not None, "the tree has a root"
    assert 1 <= len(vals) <= 10**5, "the number of nodes is in the range [1, 10^5]"
    assert all(1 <= v <= 10**4 for v in vals), "1 <= Node.val <= 10^4"
