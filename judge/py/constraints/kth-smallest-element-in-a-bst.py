"""Kth Smallest Element in a BST: a level-order binary search tree and k."""

from itertools import pairwise


def check(root: list, k: int) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has a root"
    # Level-order layout: children of the i-th real node come from the queue.
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    queue = [0]
    pos = 1
    head = 0
    while head < len(queue) and pos < len(root):
        node = queue[head]
        head += 1
        if pos < len(root):
            if root[pos] is not None:
                left[node] = pos
                queue.append(pos)
            pos += 1
        if pos < len(root):
            if root[pos] is not None:
                right[node] = pos
                queue.append(pos)
            pos += 1
    n = len(queue)
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 1 <= k <= n, "1 <= k <= n"
    assert all(isinstance(root[i], int) and 0 <= root[i] <= 10**4 for i in queue), (
        "0 <= Node.val <= 10^4"
    )
    order: list[int] = []
    stack: list[int] = []
    cur: int | None = 0
    while cur is not None or stack:
        while cur is not None:
            stack.append(cur)
            cur = left.get(cur)
        cur = stack.pop()
        order.append(root[cur])
        cur = right.get(cur)
    assert all(a <= b for a, b in pairwise(order)), "the tree is a valid binary search tree"
