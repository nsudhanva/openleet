"""Flip Equivalent Binary Trees: two binary trees in level-order form."""


def _tree_values(root: list) -> list:
    """Values of a level-order tree list, asserting the list is well formed."""
    if not root:
        return []
    assert root[0] is not None, "the root of a non-empty tree is not null"
    vals = [root[0]]
    pos, pending = 1, 1
    while pending and pos < len(root):
        level = root[pos : pos + 2 * pending]
        pos += 2 * pending
        kids = [v for v in level if v is not None]
        vals += kids
        pending = len(kids)
    assert pos >= len(root), "null nodes have no children in the level-order list"
    return vals


def check(root1: list, root2: list) -> None:
    for vals in (_tree_values(root1), _tree_values(root2)):
        assert len(vals) <= 100, "the number of nodes in each tree is in the range [0, 100]"
        assert all(0 <= v <= 99 for v in vals), "node values are in the range [0, 99]"
        assert len(set(vals)) == len(vals), "each tree has unique node values"
