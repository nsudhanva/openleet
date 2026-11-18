"""Balanced Binary Tree: a binary tree in level-order."""


def _nodes(root: list) -> tuple[int, list[tuple[int, int | None, int | None]]]:
    """Return (node count, [(value, left index, right index)]) of a level-order tree."""
    assert isinstance(root, list), "root is a level-order list"
    if not root:
        return 0, []
    assert root[0] is not None, "root is not null"
    nodes: list[list] = [[root[0], None, None]]
    queue = [0]
    pos = 1
    head = 0
    while head < len(queue):
        cur = queue[head]
        head += 1
        for side in (1, 2):
            if pos >= len(root):
                break
            v = root[pos]
            pos += 1
            if v is not None:
                nodes.append([v, None, None])
                nodes[cur][side] = len(nodes) - 1
                queue.append(len(nodes) - 1)
    return len(nodes), [tuple(n) for n in nodes]


def check(root: list) -> None:
    count, nodes = _nodes(root)
    assert 0 <= count <= 5000, "the number of nodes is in the range [0, 5000]"
    assert all(isinstance(v, int) and -(10**4) <= v <= 10**4 for v, _, _ in nodes), (
        "-10^4 <= Node.val <= 10^4"
    )
