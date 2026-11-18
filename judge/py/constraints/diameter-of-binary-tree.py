"""Diameter of Binary Tree: a level-order binary tree."""


def check(root: list[int | None]) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "the tree has a root"
    pending, pos, nodes = 1, 1, [root[0]]
    while pending and pos < len(root):
        pending -= 1
        for _ in range(2):
            if pos < len(root):
                value = root[pos]
                if value is not None:
                    pending += 1
                    nodes.append(value)
                pos += 1
    assert 1 <= len(nodes) <= 10**4, "the number of nodes is in [1, 10^4]"
    assert all(isinstance(v, int) and -100 <= v <= 100 for v in nodes), "-100 <= Node.val <= 100"
