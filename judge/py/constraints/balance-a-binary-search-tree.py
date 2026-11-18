"""Balance a Binary Search Tree: a binary search tree in level-order."""


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
    assert 1 <= count <= 10**4, "the number of nodes is in the range [1, 10^4]"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for v, _, _ in nodes), "1 <= Node.val <= 10^5"
    # the tree is a binary search tree: in-order values strictly increase
    prev = None
    stack: list[int] = []
    cur: int | None = 0
    while stack or cur is not None:
        while cur is not None:
            stack.append(cur)
            cur = nodes[cur][1]
        cur = stack.pop()
        v = nodes[cur][0]
        assert prev is None or v > prev, "the tree is a binary search tree"
        prev = v
        cur = nodes[cur][2]
