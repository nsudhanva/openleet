"""Validate Binary Search Tree: a binary tree as a level-order list with None for gaps."""


def check(root: list[int | None]) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has at least one node"
    n = sum(v is not None for v in root)
    assert 1 <= n <= 10**4, "number of nodes in [1, 10^4]"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in root if v is not None), (
        "-2^31 <= Node.val <= 2^31 - 1"
    )
