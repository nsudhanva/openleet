"""Symmetric Tree: a binary tree in level-order with None for missing children."""


def check(root: list) -> None:
    assert isinstance(root, list), "root is a level-order list"
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 1000, "number of nodes in [1, 1000]"
    assert root[0] is not None, "root is not empty"
    assert all(isinstance(v, int) and -100 <= v <= 100 for v in vals), "-100 <= Node.val <= 100"
    # level-order structure: each non-null node consumes two slots
    slots = 1
    for i, v in enumerate(root):
        assert i < slots, "valid level-order encoding"
        if v is not None:
            slots += 2
