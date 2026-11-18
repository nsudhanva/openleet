"""Kth Largest Sum in a Binary Tree: a level-order binary tree and k."""


def check(root: list, k: int) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has a root"
    vals = [v for v in root if v is not None]
    n = len(vals)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**6 for v in vals), "1 <= Node.val <= 10^6"
    assert 1 <= k <= n, "1 <= k <= n"
