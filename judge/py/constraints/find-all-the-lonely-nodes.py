"""Find All The Lonely Nodes: a binary tree as a level-order list."""

from collections import deque


def _tree(root: list) -> tuple[list[int], int]:
    """Return (non-null values, height) of a level-order tree list."""
    assert isinstance(root, list) and root and root[0] is not None, (
        "root is a non-empty level-order tree"
    )
    vals = [root[0]]
    height = 1
    queue = deque([1])
    i = 1
    while queue:
        d = queue.popleft()
        for _ in range(2):
            if i < len(root):
                v = root[i]
                i += 1
                if v is not None:
                    vals.append(v)
                    height = max(height, d + 1)
                    queue.append(d + 1)
    return vals, height


def check(root: list) -> None:
    vals, _ = _tree(root)
    assert 1 <= len(vals) <= 1000, "the number of nodes is in [1, 1000]"
    assert all(1 <= v <= 10**6 for v in vals), "1 <= Node.val <= 10^6"
