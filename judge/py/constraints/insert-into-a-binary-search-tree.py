"""Insert into a Binary Search Tree: a BST and a value not in it."""

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


def check(root: list, val: int) -> None:
    vals, left, right = _parse(root)
    assert 0 <= len(vals) <= 10**4, "number of nodes is in the range [0, 10^4]"
    assert all(isinstance(v, int) and -(10**8) <= v <= 10**8 for v in vals), (
        "-10^8 <= Node.val <= 10^8"
    )
    assert len(set(vals)) == len(vals), "All the values Node.val are unique"
    order = _inorder(vals, left, right)
    assert all(a < b for a, b in pairwise(order)), "root is a binary search tree"
    assert -(10**8) <= val <= 10**8, "-10^8 <= val <= 10^8"
    assert val not in set(vals), "val does not exist in the original BST"
