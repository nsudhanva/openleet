"""Count Complete Tree Nodes: a complete binary tree as a level-order list."""


def check(root: list) -> None:
    if not root:
        return
    assert root[0] is not None, "the root is not missing"
    vals = []
    count = 0
    seen_gap = False
    queue_pos = 0
    nodes = [0]  # positions in the list of the nodes, level order
    i = 1
    while queue_pos < len(nodes):
        queue_pos += 1
        for _ in range(2):
            if i >= len(root):
                seen_gap = True
                continue
            v = root[i]
            i += 1
            if v is None:
                seen_gap = True
            else:
                assert not seen_gap, "the tree is complete"
                nodes.append(i - 1)
    vals = [root[p] for p in nodes]
    count = len(vals)
    assert 0 <= count <= 5 * 10**4, "number of nodes in [0, 5 * 10^4]"
    assert all(isinstance(v, int) and 0 <= v <= 5 * 10**4 for v in vals), (
        "0 <= Node.val <= 5 * 10^4"
    )
