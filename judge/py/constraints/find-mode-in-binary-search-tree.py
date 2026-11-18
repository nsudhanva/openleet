"""Find Mode in Binary Search Tree: a BST with duplicates, level-order."""


def check(root: list[int | None]) -> None:
    root = list(root)
    while root and root[-1] is None:
        root.pop()  # trailing nulls do not change the tree
    assert 1 <= len(root) <= 10**5 and root[0] is not None, "tree has a root"
    # Build the tree from the level-order list (LeetCode format).
    left: list[int] = []
    right: list[int] = []
    vals: list[int] = []
    queue = [0]
    vals.append(root[0])
    left.append(-1)
    right.append(-1)
    pos = 1
    head = 0
    while head < len(queue):
        cur = queue[head]
        head += 1
        for side in (left, right):
            if pos >= len(root):
                break
            v = root[pos]
            pos += 1
            if v is not None:
                vals.append(v)
                left.append(-1)
                right.append(-1)
                side[cur] = len(vals) - 1
                queue.append(len(vals) - 1)
    assert pos >= len(root), "level-order list has no entries beyond the tree"
    n = len(vals)
    assert 1 <= n <= 10**4, "number of nodes in [1, 10^4]"
    assert all(-(10**5) <= v <= 10**5 for v in vals), "-10^5 <= Node.val <= 10^5"
    # BST with duplicates: in-order traversal is non-decreasing.
    stack: list[int] = []
    cur = 0
    prev = None
    while stack or cur != -1:
        while cur != -1:
            stack.append(cur)
            cur = left[cur]
        cur = stack.pop()
        assert prev is None or prev <= vals[cur], "the tree is a valid BST (duplicates allowed)"
        prev = vals[cur]
        cur = right[cur]
