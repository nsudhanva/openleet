"""Merge Two Binary Trees: two binary trees in level-order lists."""


def check(root1: list, root2: list) -> None:
    for t in (root1, root2):
        assert sum(v is not None for v in t) <= 2000, "number of nodes in [0, 2000]"
        assert all(v is None or -(10**4) <= v <= 10**4 for v in t), "-10^4 <= Node.val <= 10^4"
