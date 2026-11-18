"""Populating Next Right Pointers in Each Node: a perfect binary tree in level order."""

from typing import cast


def check(root: list[int | None]) -> None:
    n = len(root)
    assert n <= 2**12 - 1, "number of nodes is in [0, 2^12 - 1]"
    assert (n + 1) & n == 0, "the tree is perfect: every level is full"
    assert all(v is not None for v in root), "the tree is perfect: no missing children"
    assert all(-1000 <= v <= 1000 for v in cast(list[int], root)), "-1000 <= Node.val <= 1000"
