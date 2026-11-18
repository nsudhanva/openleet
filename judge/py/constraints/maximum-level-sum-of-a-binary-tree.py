"""Maximum Level Sum of a Binary Tree: a level-order binary tree."""


def check(root: list[int | None]) -> None:
    count = sum(v is not None for v in root)
    assert 1 <= count <= 10**4, "number of nodes in [1, 10^4]"
    assert root[0] is not None, "root is not null"
    assert all(v is None or -(10**5) <= v <= 10**5 for v in root), "-10^5 <= Node.val <= 10^5"
