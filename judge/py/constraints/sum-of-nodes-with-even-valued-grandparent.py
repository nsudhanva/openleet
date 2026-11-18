"""Sum of Nodes with Even-Valued Grandparent: a binary tree."""


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
    assert 1 <= len(vals) <= 10**4, "number of nodes in [1, 10**4]"
    assert all(1 <= v <= 100 for v in vals), "1 <= Node.val <= 100"
