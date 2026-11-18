"""Delete Node in a BST: a binary search tree (level order) with unique values, and a key."""


def _attach(t: list) -> tuple[list[int], dict[int, int], dict[int, int]]:
    """Values of the nodes a level-order list really builds, with left/right child positions."""
    if not t or t[0] is None:
        return [], {}, {}
    vals = [t[0]]
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    queue = [0]
    head = 0
    i = 1
    while head < len(queue) and i < len(t):
        p = queue[head]
        head += 1
        for side in (left, right):
            if i < len(t) and t[i] is not None:
                vals.append(t[i])
                side[p] = len(vals) - 1
                queue.append(len(vals) - 1)
            i += 1
    return vals, left, right


def check(root: list[int | None], key: int) -> None:
    assert isinstance(root, list), "root is a level-order list"
    vals, left, right = _attach(root)
    assert len(vals) <= 10**4, "the number of nodes in the tree is in the range [0, 10^4]"
    assert all(-(10**5) <= v <= 10**5 for v in vals), "-10^5 <= Node.val <= 10^5"
    order = []
    stack: list[int] = []
    cur = 0 if vals else None
    while stack or cur is not None:
        while cur is not None:
            stack.append(cur)
            cur = left.get(cur)
        cur = stack.pop()
        order.append(vals[cur])
        cur = right.get(cur)
    assert all(order[i] < order[i + 1] for i in range(len(order) - 1)), (
        "each node has a unique value and root is a valid binary search tree"
    )
    assert -(10**5) <= key <= 10**5, "-10^5 <= key <= 10^5"
