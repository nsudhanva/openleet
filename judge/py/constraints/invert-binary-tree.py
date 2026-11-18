"""Invert Binary Tree: a level-order binary tree."""


def check(root: list[int | None]) -> None:
    assert isinstance(root, list), "tree is a level-order list"
    if root:
        assert root[0] is not None, "root is not null"
    count = sum(v is not None for v in root)
    assert 0 <= count <= 100, "number of nodes in [0, 100]"
    assert all(-100 <= v <= 100 for v in root if v is not None), "-100 <= Node.val <= 100"
