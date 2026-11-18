"""Delete Leaves With a Given Value: a binary tree (level order) and a target value."""


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


def check(root: list[int | None], target: int) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "the tree is non-empty"
    vals, _, _ = _attach(root)
    assert 1 <= len(vals) <= 3000, "the number of nodes in the tree is in the range [1, 3000]"
    assert all(1 <= v <= 1000 for v in vals), "1 <= Node.val <= 1000"
    assert 1 <= target <= 1000, "1 <= target <= 1000"
