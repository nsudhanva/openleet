"""Insufficient Nodes in Root to Leaf Paths: a level-order binary tree and a limit."""


def check(root: list[int | None], limit: int) -> None:
    assert isinstance(root, list) and root, "tree is a non-empty level-order list"
    assert root[0] is not None, "root is not null"
    count = sum(v is not None for v in root)
    assert 1 <= count <= 5000, "number of nodes in [1, 5000]"
    assert all(-(10**5) <= v <= 10**5 for v in root if v is not None), "-10^5 <= Node.val <= 10^5"
    assert -(10**9) <= limit <= 10**9, "-10^9 <= limit <= 10^9"
