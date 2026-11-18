"""Flatten Binary Tree to Linked List: a binary tree in level-order form."""


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


def check(root: list) -> None:
    vals = _tree_values(root)
    assert 0 <= len(vals) <= 2000, "the number of nodes is in the range [0, 2000]"
    assert all(-100 <= v <= 100 for v in vals), "-100 <= Node.val <= 100"
