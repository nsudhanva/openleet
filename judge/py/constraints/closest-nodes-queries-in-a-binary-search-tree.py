"""Closest Nodes Queries in a Binary Search Tree: a BST in level order and queries."""


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


def check(root: list, queries: list[int]) -> None:
    vals = _bst_values(root)
    assert 2 <= len(vals) <= 10**5, "the number of nodes is in [2, 10^5]"
    assert all(1 <= v <= 10**6 for v in vals), "1 <= Node.val <= 10^6"
    assert 1 <= len(queries) <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= q <= 10**6 for q in queries), "1 <= queries[i] <= 10^6"
