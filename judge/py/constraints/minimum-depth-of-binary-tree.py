"""Minimum Depth of Binary Tree: a level-order binary tree."""


def check(root: list) -> None:
    assert sum(v is not None for v in root) <= 10**5, "the number of nodes is in [0, 10^5]"
    assert all(v is None or (isinstance(v, int) and -1000 <= v <= 1000) for v in root), (
        "-1000 <= Node.val <= 1000"
    )
    if root:
        assert root[0] is not None, "the root is not missing"
