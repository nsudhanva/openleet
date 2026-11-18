"""Closest Binary Search Tree Value II: a BST in level order, a target and k."""


def _bst_values(root: list) -> list:
    """In-order values of a level-order tree, without recursion."""
    n = len(root)
    assert n >= 1 and root[0] is not None, "root is not empty"
    left = [-1] * n
    right = [-1] * n
    queue = [0]
    nxt = 1
    for i in queue:
        for side in (left, right):
            if nxt < n:
                if root[nxt] is not None:
                    side[i] = nxt
                    queue.append(nxt)
                nxt += 1
    assert len(queue) == len([v for v in root if v is not None]), "well-formed tree"
    out = []
    stack = []
    cur = 0
    while stack or cur != -1:
        while cur != -1:
            stack.append(cur)
            cur = left[cur]
        cur = stack.pop()
        out.append(root[cur])
        cur = right[cur]
    assert all(out[i] <= out[i + 1] for i in range(len(out) - 1)), (
        "the tree is a binary search tree"
    )
    return out


def check(root: list, target: float, k: int) -> None:
    vals = _bst_values(root)
    n = len(vals)
    assert 1 <= k <= n <= 10**4, "1 <= k <= n <= 10^4"
    assert all(0 <= v <= 10**9 for v in vals), "0 <= Node.val <= 10^9"
    assert -(10**9) <= target <= 10**9, "-10^9 <= target <= 10^9"
    if k < n:
        dist = sorted(abs(v - target) for v in vals)
        assert dist[k - 1] < dist[k], "only one unique set of k closest values"
