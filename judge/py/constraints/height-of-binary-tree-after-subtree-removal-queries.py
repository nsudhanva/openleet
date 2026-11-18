"""Height of Binary Tree After Subtree Removal Queries: a tree of values 1..n and queries."""

from collections import deque


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


def check(root: list, queries: list[int]) -> None:
    vals, _, _ = _parse(root)
    n = len(vals)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= n for v in vals), "1 <= Node.val <= n"
    assert len(set(vals)) == n, "All the values in the tree are unique"
    m = len(queries)
    assert 1 <= m <= min(n, 10**4), "1 <= m <= min(n, 10^4)"
    assert all(1 <= q <= n for q in queries), "1 <= queries[i] <= n"
    assert all(q != vals[0] for q in queries), "queries[i] != root.val"
