"""Count Good Nodes in Binary Tree: a non-empty binary tree as a level-order list."""


def check(root: list) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has a root"
    nodes = 1
    pending = 1  # nodes in the queue that still need two child slots
    i = 1
    vals = [root[0]]
    while pending and i < len(root):
        pending -= 1
        for _ in range(2):
            if i < len(root):
                v = root[i]
                i += 1
                if v is not None:
                    vals.append(v)
                    pending += 1
    nodes = len(vals)
    assert 1 <= nodes <= 10**5, "number of nodes in [1, 10^5]"
    assert all(isinstance(v, int) and -(10**4) <= v <= 10**4 for v in vals), (
        "-10^4 <= Node.val <= 10^4"
    )
