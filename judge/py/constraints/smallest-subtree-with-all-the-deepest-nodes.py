"""Smallest Subtree with all the Deepest Nodes: a level-order binary tree of unique values."""


def check(root: list) -> None:
    assert root and root[0] is not None, "the tree has a root"
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 500, "number of nodes is in the range [1, 500]"
    assert all(isinstance(v, int) and 0 <= v <= 500 for v in vals), "0 <= Node.val <= 500"
    assert len(set(vals)) == len(vals), "node values are unique"
