"""Evaluate Boolean Binary Tree: a full binary tree as a level-order list."""


def check(root: list) -> None:
    assert isinstance(root, list) and root, "root is a non-empty level-order list"
    assert root[0] is not None, "the tree has a root"
    nodes = 0
    pos = 1  # index of the next child slot in the list
    for v in root:
        if v is None:
            continue
        assert isinstance(v, int) and 0 <= v <= 3, "0 <= Node.val <= 3"
        nodes += 1
        left = root[pos] if pos < len(root) else None
        right = root[pos + 1] if pos + 1 < len(root) else None
        pos += 2
        assert (left is None) == (right is None), "every node has either 0 or 2 children"
        if left is None:
            assert v in (0, 1), "leaf nodes have a value of 0 or 1"
        else:
            assert v in (2, 3), "non-leaf nodes have a value of 2 or 3"
    assert pos >= len(root), "level-order list has entries without a parent"
    assert 1 <= nodes <= 1000, "the number of nodes is in the range [1, 1000]"
