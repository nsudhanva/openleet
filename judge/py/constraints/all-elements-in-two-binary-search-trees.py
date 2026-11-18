"""All Elements in Two Binary Search Trees: two BSTs in level-order form."""

from itertools import pairwise


def _tree_values(tree: list, name: str) -> list[int]:
    assert isinstance(tree, list), f"{name} is a level-order list"
    tree = list(tree)
    while tree and tree[-1] is None:
        tree.pop()
    if not tree:
        return []
    assert tree[0] is not None, f"{name} root is not missing"
    values = [v for v in tree if v is not None]
    # each present node consumes two child slots; the list has no slots beyond those
    assert len(tree) <= 1 + 2 * len(values), f"{name} is a valid level-order tree"
    return values


def _is_bst(tree: list) -> bool:
    # level-order -> child links, then iterative in-order traversal
    n = len(tree)
    left = [-1] * n
    right = [-1] * n
    queue = [0]
    nxt = 1
    for i in queue:
        for side in (left, right):
            if nxt < n:
                if tree[nxt] is not None:
                    side[i] = nxt
                    queue.append(nxt)
                nxt += 1
    out: list[int] = []
    stack: list[int] = []
    cur = 0
    while stack or cur != -1:
        while cur != -1:
            stack.append(cur)
            cur = left[cur]
        cur = stack.pop()
        out.append(tree[cur])
        cur = right[cur]
    return all(a <= b for a, b in pairwise(out))


def check(root1: list[int | None], root2: list[int | None]) -> None:
    for name, tree in (("root1", root1), ("root2", root2)):
        values = _tree_values(tree, name)
        assert len(values) <= 5000, "The number of nodes in each tree is in the range [0, 5000]"
        assert all(isinstance(v, int) and -(10**5) <= v <= 10**5 for v in values), (
            "-10^5 <= Node.val <= 10^5"
        )
        if values:
            assert _is_bst(tree), f"{name} is a binary search tree"
