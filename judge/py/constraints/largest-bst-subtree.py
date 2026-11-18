"""Largest BST Subtree: a binary tree as a level-order list with None for missing children."""


def check(root: list) -> None:
    assert isinstance(root, list), "tree is a level-order list"
    pending = 1
    for v in root:
        assert pending > 0, "valid level-order tree"
        pending += 2 * (v is not None) - 1
    nodes = [v for v in root if v is not None]
    assert len(nodes) <= 10**4, "number of nodes is in [0, 10^4]"
    assert all(type(v) is int for v in nodes), "values are integers"
    assert all(-(10**4) <= v <= 10**4 for v in nodes), "-10^4 <= Node.val <= 10^4"
