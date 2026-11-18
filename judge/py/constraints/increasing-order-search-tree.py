"""Increasing Order Search Tree: a binary search tree."""

from collections import deque
from itertools import pairwise


def _parse(tree: list) -> tuple[list[int], list[int], list[int]]:
    """Return node values and left/right child indices (-1 for none) of a level-order tree."""
    assert isinstance(tree, list), "tree is a level-order list"
    if not tree:
        return [], [], []
    assert tree[0] is not None, "root is not null"
    vals, left, right = [tree[0]], [-1], [-1]
    queue = deque([0])
    i = 1
    while queue:
        node = queue.popleft()
        for kids in (left, right):
            if i < len(tree):
                v = tree[i]
                i += 1
                if v is not None:
                    kids[node] = len(vals)
                    queue.append(len(vals))
                    vals.append(v)
                    left.append(-1)
                    right.append(-1)
    return vals, left, right


def _inorder(vals: list[int], left: list[int], right: list[int]) -> list[int]:
    out, stack, cur = [], [], 0 if vals else -1
    while stack or cur != -1:
        while cur != -1:
            stack.append(cur)
            cur = left[cur]
        cur = stack.pop()
        out.append(vals[cur])
        cur = right[cur]
    return out


def check(root: list) -> None:
    vals, left, right = _parse(root)
    assert 1 <= len(vals) <= 100, "number of nodes is in the range [1, 100]"
    assert all(isinstance(v, int) and 0 <= v <= 1000 for v in vals), "0 <= Node.val <= 1000"
    order = _inorder(vals, left, right)
    assert all(a <= b for a, b in pairwise(order)), "root is a binary search tree"
