"""Maximum Sum BST in Binary Tree: a binary tree as a level-order list with None gaps."""


def check(root: list[int | None]) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has at least one node"
    # Read the tree the way LeetCode does: only nodes reachable from the root count.
    reachable = [root[0]]
    queue_start = 0
    i = 1
    while queue_start < len(reachable) and i < len(root):
        queue_start += 1
        for _ in range(2):
            value = root[i] if i < len(root) else None
            if value is not None:
                reachable.append(value)
            i += 1
    assert 1 <= len(reachable) <= 4 * 10**4, "node count in [1, 4 * 10^4]"
    assert all(-4 * 10**4 <= v <= 4 * 10**4 for v in reachable), "-4 * 10^4 <= Node.val <= 4 * 10^4"
