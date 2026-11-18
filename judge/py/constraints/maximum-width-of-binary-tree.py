"""Maximum Width of Binary Tree: a binary tree as a level-order list with None for gaps."""


def check(root: list[int | None]) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "the tree has a root"
    # Read the tree the way the judge does: only nodes attached to the root count.
    reachable = [root[0]]
    head, pos = 0, 1
    while head < len(reachable) and pos < len(root):
        head += 1
        for _ in range(2):
            value = root[pos] if pos < len(root) else None
            if value is not None:
                reachable.append(value)
            pos += 1
    assert 1 <= len(reachable) <= 3000, "number of nodes in [1, 3000]"
    assert all(-100 <= v <= 100 for v in reachable), "-100 <= Node.val <= 100"
