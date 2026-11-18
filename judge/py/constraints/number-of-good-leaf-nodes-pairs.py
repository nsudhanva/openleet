"""Number of Good Leaf Nodes Pairs: a binary tree in level order and a distance."""

from collections import deque


def check(root: list, distance: int) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree is non-empty"
    # Walk the level-order list the way the harness builds the tree; only nodes it
    # attaches belong to the tree.
    vals = [root[0]]
    queue = deque([0])
    i = 1
    while queue and i < len(root):
        queue.popleft()
        for _ in range(2):
            if i < len(root) and root[i] is not None:
                vals.append(root[i])
                queue.append(i)
            i += 1
    assert 1 <= len(vals) <= 2**10, "the number of nodes is in the range [1, 2^10]"
    assert all(isinstance(v, int) and 1 <= v <= 100 for v in vals), "1 <= Node.val <= 100"
    assert 1 <= distance <= 10, "1 <= distance <= 10"
