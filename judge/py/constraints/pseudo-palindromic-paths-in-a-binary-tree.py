"""Pseudo-Palindromic Paths in a Binary Tree: a level-order binary tree of digits 1 to 9."""


def check(root: list) -> None:
    assert isinstance(root, list) and root, "the tree has at least one node"
    assert root[0] is not None, "the root is not null"
    nodes = [v for v in root if v is not None]
    assert 1 <= len(nodes) <= 10**5, "the number of nodes is in the range [1, 10^5]"
    assert all(isinstance(v, int) and 1 <= v <= 9 for v in nodes), "1 <= Node.val <= 9"
