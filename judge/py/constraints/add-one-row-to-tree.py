"""Add One Row to Tree: a level-order binary tree, a value and a depth."""


def check(root: list, val: int, depth: int) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "the tree is non-empty"
    nodes = 0
    level = 1
    height = 0
    i = 0
    n = len(root)
    while level and i < n:
        height += 1
        chunk = root[i : i + level]
        present = sum(v is not None for v in chunk)
        nodes += present
        i += level
        level = 2 * present
    assert i >= n, "level-order list is well formed"
    assert all(v is None or (isinstance(v, int) and -100 <= v <= 100) for v in root), (
        "-100 <= Node.val <= 100"
    )
    assert 1 <= nodes <= 10**4, "The number of nodes in the tree is in the range [1, 10^4]"
    assert 1 <= height <= 10**4, "The depth of the tree is in the range [1, 10^4]"
    assert -(10**5) <= val <= 10**5, "-10^5 <= val <= 10^5"
    assert 1 <= depth <= height + 1, "1 <= depth <= the depth of tree + 1"
