"""Construct String from Binary Tree: a binary tree in level-order form."""


def check(root: list) -> None:
    assert root and root[0] is not None, "the tree has at least one node"
    nodes = [v for v in root if v is not None]
    assert 1 <= len(nodes) <= 10**4, "The number of nodes in the tree is in the range [1, 10^4]"
    assert all(-1000 <= v <= 1000 for v in nodes), "-1000 <= Node.val <= 1000"
