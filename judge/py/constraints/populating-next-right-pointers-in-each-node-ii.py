"""Populating Next Right Pointers in Each Node II: a binary tree in level order."""


def check(root: list[int | None]) -> None:
    assert all(v is None or isinstance(v, int) for v in root), "node values are integers"
    assert root == [] or root[0] is not None, "the root is not missing"
    # Level-order shape: each present node consumes two slots (its children).
    pos = 1
    present = 0
    for i, v in enumerate(root):
        if v is None:
            continue
        present += 1
        if i >= pos:
            raise AssertionError("level-order list is a valid tree")
        pos += 2
    assert pos >= len(root) or root == [], "level-order list is a valid tree"
    assert present <= 6000, "number of nodes is in [0, 6000]"
    assert all(-100 <= v <= 100 for v in root if v is not None), "-100 <= Node.val <= 100"
