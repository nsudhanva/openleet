"""Count Nodes Equal to Sum of Descendants: a binary tree in level order."""


def check(root: list[int | None]) -> None:
    assert len(root) >= 1 and root[0] is not None, "tree is non-empty"
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 10**5, "number of nodes in [1, 10^5]"
    assert all(0 <= v <= 10**5 for v in vals), "0 <= Node.val <= 10^5"
