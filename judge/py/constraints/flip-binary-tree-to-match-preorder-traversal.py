"""Flip Binary Tree To Match Preorder Traversal: a tree of n nodes valued 1..n and a voyage
of n unique values."""


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


def check(root: list, voyage: list[int]) -> None:
    vals = _tree_values(root)
    n = len(vals)
    assert n == len(voyage), "n == voyage.length"
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(1 <= v <= n for v in vals), "1 <= Node.val <= n"
    assert all(1 <= v <= n for v in voyage), "1 <= voyage[i] <= n"
    assert len(set(vals)) == n, "all the values in the tree are unique"
    assert len(set(voyage)) == n, "all the values in voyage are unique"
