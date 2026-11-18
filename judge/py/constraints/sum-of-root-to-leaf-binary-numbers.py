"""Sum of Root To Leaf Binary Numbers: a binary tree of 0/1 nodes."""


def _tree(root: list) -> tuple[list[int], int]:
    """Return (node values, depth in levels) of a level-order tree, asserting its shape."""
    assert isinstance(root, list) and root and root[0] is not None, "tree has a root"
    vals = [root[0]]
    level, pos, depth = 1, 1, 0
    while level:
        depth += 1
        slots = root[pos : pos + 2 * level]
        pos += 2 * level
        kids = [v for v in slots if v is not None]
        vals += kids
        level = len(kids)
    assert pos >= len(root), "children of missing nodes are not listed"
    return vals, depth


def check(root: list) -> None:
    vals, _depth = _tree(root)
    assert 1 <= len(vals) <= 1000, "number of nodes in [1, 1000]"
    assert all(0 <= v <= 1 for v in vals), "Node.val is 0 or 1"
