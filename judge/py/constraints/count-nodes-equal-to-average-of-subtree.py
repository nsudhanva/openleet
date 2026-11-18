"""Count Nodes Equal to Average of Subtree: a binary tree in level order."""


def check(root: list[int | None]) -> None:
    assert len(root) >= 1 and root[0] is not None, "tree is non-empty"
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 1000, "number of nodes in [1, 1000]"
    assert all(0 <= v <= 1000 for v in vals), "0 <= Node.val <= 1000"
