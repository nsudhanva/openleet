"""Maximum Average Subtree: a binary tree in level order."""


def check(root: list[int | None]) -> None:
    assert root and root[0] is not None, "the root exists"
    nodes = [v for v in root if v is not None]
    assert 1 <= len(nodes) <= 10**4, "number of nodes in [1, 10^4]"
    assert all(0 <= v <= 10**5 for v in nodes), "0 <= Node.val <= 10^5"
