"""Two Sum BSTs: two binary search trees and a target."""

from itertools import pairwise


def _tree(root: list) -> tuple[list, list, list]:
    """Parse a level-order list into (values, left, right) index arrays."""
    assert isinstance(root, list) and root and root[0] is not None, "root list starts with a node"
    vals, left, right = [root[0]], [-1], [-1]
    queue, i = [0], 1
    head = 0
    while head < len(queue):
        cur = queue[head]
        head += 1
        for side in (left, right):
            if i < len(root):
                v = root[i]
                i += 1
                if v is not None:
                    vals.append(v)
                    left.append(-1)
                    right.append(-1)
                    side[cur] = len(vals) - 1
                    queue.append(len(vals) - 1)
    assert i == len(root), "well-formed level-order tree"
    return vals, left, right


def _inorder(vals: list, left: list, right: list) -> list:
    out, stack, cur = [], [], 0
    while stack or cur != -1:
        while cur != -1:
            stack.append(cur)
            cur = left[cur]
        cur = stack.pop()
        out.append(vals[cur])
        cur = right[cur]
    return out


def check(root1: list, root2: list, target: int) -> None:
    for root in (root1, root2):
        vals, left, right = _tree(root)
        assert 1 <= len(vals) <= 5000, "nodes in each tree in [1, 5000]"
        assert all(-(10**9) <= v <= 10**9 for v in vals), "-10^9 <= Node.val <= 10^9"
        order = _inorder(vals, left, right)
        assert all(a <= b for a, b in pairwise(order)), "each tree is a binary search tree"
    assert -(10**9) <= target <= 10**9, "-10^9 <= target <= 10^9"
