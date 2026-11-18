"""Binary Tree Coloring Game: a tree of n distinct values 1..n, plus n and x."""


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


def check(root: list, n: int, x: int) -> None:
    assert isinstance(n, int) and isinstance(x, int), "n and x are integers"
    vals, _, _ = _parse(root)
    assert len(vals) == n, "the number of nodes in the tree is n"
    assert 1 <= x <= n <= 100, "1 <= x <= n <= 100"
    assert n % 2 == 1, "n is odd"
    assert all(1 <= v <= n for v in vals), "1 <= Node.val <= n"
    assert len(set(vals)) == len(vals), "all the values of the tree are unique"
