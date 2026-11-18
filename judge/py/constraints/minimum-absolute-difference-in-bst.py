"""Minimum Absolute Difference in BST: a binary search tree as a level-order list."""


def check(root: list) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree is not empty"
    # Parse LeetCode level-order format: children of None nodes are omitted.
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    queue = [0]
    head = 0
    nxt = 1
    while head < len(queue) and nxt < len(root):
        node = queue[head]
        head += 1
        if nxt < len(root):
            if root[nxt] is not None:
                left[node] = nxt
                queue.append(nxt)
            nxt += 1
        if nxt < len(root):
            if root[nxt] is not None:
                right[node] = nxt
                queue.append(nxt)
            nxt += 1
    count = sum(v is not None for v in root)
    assert 2 <= count <= 10**4, "the number of nodes is in the range [2, 10^4]"
    assert len(queue) == count, "the list is a valid level-order tree"
    assert all(v is None or 0 <= v <= 10**5 for v in root), "0 <= Node.val <= 10^5"
    # Iterative BST validation with value bounds.
    stack = [(0, float("-inf"), float("inf"))]
    while stack:
        node, lo, hi = stack.pop()
        val = root[node]
        assert lo < val < hi, "the tree is a binary search tree"
        if node in left:
            stack.append((left[node], lo, val))
        if node in right:
            stack.append((right[node], val, hi))
