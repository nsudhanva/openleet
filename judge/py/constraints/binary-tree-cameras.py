"""Binary Tree Cameras: a binary tree of zeros as a level-order list."""


def _parse(root: list) -> tuple[list[int], dict[int, int], dict[int, int]]:
    """Assert root is a well-formed level-order tree; return (values, left, right) by index."""
    assert isinstance(root, list), "root is a level-order list"
    assert all(v is None or isinstance(v, int) for v in root), "node values are integers or null"
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    if not root:
        return [], left, right
    assert root[0] is not None, "the root is not null"
    pos, queue = 1, [0]
    for i in queue:
        if root[i] is None:
            continue
        for side in (left, right):
            if pos < len(root):
                side[i] = pos
                queue.append(pos)
                pos += 1
    assert pos == len(root), "well-formed level-order tree"
    return [v for v in root if v is not None], left, right


def _inorder(root: list, left: dict[int, int], right: dict[int, int]) -> list[int]:
    out, stack, cur = [], [], 0 if root else None
    while stack or cur is not None:
        while cur is not None and root[cur] is not None:
            stack.append(cur)
            cur = left.get(cur)
        if not stack:
            break
        cur = stack.pop()
        out.append(root[cur])
        cur = right.get(cur)
    return out


def check(root: list) -> None:
    vals, _, _ = _parse(root)
    assert 1 <= len(vals) <= 1000, "the number of nodes is in [1, 1000]"
    assert all(v == 0 for v in vals), "Node.val == 0"
