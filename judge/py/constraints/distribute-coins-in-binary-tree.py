"""Distribute Coins in Binary Tree: a level-order tree whose coin counts sum to the node count."""


def check(root: list) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has a root"
    # level-order: each non-null node consumes two slots for its children
    slots = 1
    for i, v in enumerate(root):
        assert i < slots, "level-order list has no slots without a parent"
        if v is not None:
            slots += 2
    nodes = [v for v in root if v is not None]
    n = len(nodes)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(isinstance(v, int) and 0 <= v <= n for v in nodes), "0 <= Node.val <= n"
    assert sum(nodes) == n, "the sum of all Node.val is n"
