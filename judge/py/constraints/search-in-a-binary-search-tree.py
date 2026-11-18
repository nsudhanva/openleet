"""Search in a Binary Search Tree: a BST as a level-order list with None gaps, plus a value."""

from typing import cast


def check(root: list[int | None], val: int) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "root is non-empty"
    # Parse the level-order list into children indices.
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    queue = [0]
    head = 0
    pos = 1
    while head < len(queue):
        i = queue[head]
        head += 1
        for side in (left, right):
            if pos < len(root):
                if root[pos] is not None:
                    side[i] = pos
                    queue.append(pos)
                pos += 1
    assert pos >= len(root), "level-order list has no stray values"
    nodes = [v for v in root if v is not None]
    assert len(nodes) == len(queue), "level-order list is well formed"
    assert 1 <= len(nodes) <= 5000, "number of nodes in [1, 5000]"
    assert all(isinstance(v, int) and 1 <= v <= 10**7 for v in nodes), "1 <= Node.val <= 10^7"
    assert 1 <= val <= 10**7, "1 <= val <= 10^7"
    # BST: iterative in-order traversal must be strictly increasing.
    prev = None
    stack: list[int] = []
    cur: int | None = 0
    while stack or cur is not None:
        while cur is not None:
            stack.append(cur)
            cur = left.get(cur)
        cur = stack.pop()
        assert prev is None or cast(int, root[cur]) > prev, "root is a binary search tree"
        prev = root[cur]
        cur = right.get(cur)
