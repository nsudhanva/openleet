"""Boundary of Binary Tree: a binary tree as a level-order list."""


def _tree(root: list) -> tuple[list[int], list[int], list[int]]:
    """Level-order list -> (values, left, right) of the tree LeetCode's builder makes."""
    assert isinstance(root, list), "root is a level-order list"
    assert all(v is None or (isinstance(v, int) and not isinstance(v, bool)) for v in root), (
        "every entry is an integer or null"
    )
    if not root:
        return [], [], []
    assert root[0] is not None, "the root is not null"
    vals, left, right = [root[0]], [-1], [-1]
    queue, head, i = [0], 0, 1
    while head < len(queue) and i < len(root):
        p = queue[head]
        head += 1
        for side in (left, right):
            if i < len(root):
                if root[i] is not None:
                    vals.append(root[i])
                    left.append(-1)
                    right.append(-1)
                    side[p] = len(vals) - 1
                    queue.append(len(vals) - 1)
                i += 1
    return vals, left, right


def check(root: list) -> None:
    vals, *_ = _tree(root)
    assert 1 <= len(vals) <= 10000, "number of nodes in [1, 10000]"
    assert all(-1000 <= v <= 1000 for v in root if v is not None), "-1000 <= Node.val <= 1000"
