"""Lowest Common Ancestor of Deepest Leaves: a binary tree as a level-order list."""


def _tree_values(root: list) -> list[int]:
    assert isinstance(root, list), "root is a level-order list"
    assert root and root[0] is not None, "the tree has a root"
    assert all(v is None or isinstance(v, int) for v in root), "node values are integers"
    pending = 1  # child slots opened by real nodes and not yet listed
    for v in root:
        assert pending > 0, "level-order list lists a child under a missing node"
        pending -= 1
        if v is not None:
            pending += 2
    return [v for v in root if v is not None]


def check(root: list) -> None:
    vals = _tree_values(root)
    assert 1 <= len(vals) <= 1000, "number of nodes in [1, 1000]"
    assert all(0 <= v <= 1000 for v in vals), "0 <= Node.val <= 1000"
    assert len(set(vals)) == len(vals), "node values are unique"
