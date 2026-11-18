"""Find Distance in a Binary Tree: a binary tree as a level-order list, and two node values."""

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


def check(root: list, p: int, q: int) -> None:
    vals, _ = _tree(root)
    assert 1 <= len(vals) <= 10**4, "the number of nodes is in [1, 10^4]"
    assert all(0 <= v <= 10**9 for v in vals), "0 <= Node.val <= 10^9"
    assert len(set(vals)) == len(vals), "all Node.val are unique"
    assert p in vals and q in vals, "p and q are values in the tree"
