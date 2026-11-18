"""Find the Level of Tree with Minimum Sum: a binary tree in level-order with None gaps."""


def check(root: list) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "root exists"
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 10**5, "number of nodes in [1, 10^5]"
    assert all(isinstance(v, int) and 1 <= v <= 10**9 for v in vals), "1 <= Node.val <= 10^9"
