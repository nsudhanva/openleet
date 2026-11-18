"""Check Completeness of a Binary Tree: a level-order list with None for missing children."""


def check(root: list[int | None]) -> None:
    assert isinstance(root, list) and root, "root is a non-empty level-order list"
    assert root[0] is not None, "the tree has at least one node"
    assert all(v is None or (isinstance(v, int) and 1 <= v <= 1000) for v in root), (
        "1 <= Node.val <= 1000"
    )
    assert 1 <= sum(v is not None for v in root) <= 100, "number of nodes in [1, 100]"
    # every present node takes two child slots; the list must be exactly consumed
    pos, queued = 0, 1
    while queued and pos < len(root):
        queued -= 1
        if root[pos] is not None:
            queued += 2
        pos += 1
    assert pos == len(root), "a valid level-order tree"
