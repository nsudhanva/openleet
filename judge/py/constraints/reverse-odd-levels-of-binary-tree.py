"""Reverse Odd Levels of Binary Tree: a perfect binary tree in level-order."""

from typing import cast


def check(root: list[int | None]) -> None:
    n = len(root)
    assert 1 <= n <= 2**14, "number of nodes is in [1, 2^14]"
    assert all(v is not None for v in root), "root is a perfect binary tree"
    assert (n + 1) & n == 0, "root is a perfect binary tree"
    assert all(0 <= v <= 10**5 for v in cast(list[int], root)), "0 <= Node.val <= 10^5"
