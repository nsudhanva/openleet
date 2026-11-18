"""Recover Binary Search Tree: a level-order BST with two values swapped."""


def check(root: list) -> None:
    assert isinstance(root, list) and root, "root is a non-empty level-order list"
    assert root[0] is not None, "the root exists"
    left, right = {}, {}
    queue, i = [0], 1
    pos = 0
    while pos < len(queue):
        node = queue[pos]
        pos += 1
        for side in (left, right):
            if i < len(root):
                if root[i] is not None:
                    side[node] = i
                    queue.append(i)
                i += 1
    assert i == len(root) and len(queue) == sum(v is not None for v in root), (
        "valid level-order list"
    )
    n = len(queue)
    assert 2 <= n <= 1000, "number of nodes in [2, 1000]"
    assert all(-(2**31) <= v <= 2**31 - 1 for v in root if v is not None), (
        "-2^31 <= Node.val <= 2^31 - 1"
    )
    order, stack, cur = [], [], 0
    while stack or cur is not None:
        while cur is not None:
            stack.append(cur)
            cur = left.get(cur)
        cur = stack.pop()
        order.append(root[cur])
        cur = right.get(cur)
    assert len(set(order)) == n, "BST values are distinct"
    diff = sum(a != b for a, b in zip(order, sorted(order), strict=True))
    assert diff == 2, "exactly two nodes of a BST were swapped"
