"""Univalued Binary Tree: a level-order binary tree."""


def check(root: list) -> None:
    assert isinstance(root, list) and root, "root is a non-empty level-order list"
    assert root[0] is not None, "root is not null"
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 100, "number of nodes in [1, 100]"
    assert all(isinstance(v, int) and 0 <= v < 100 for v in vals), "0 <= Node.val < 100"
