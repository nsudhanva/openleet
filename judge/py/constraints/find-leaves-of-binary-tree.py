"""Find Leaves of Binary Tree: a non-empty binary tree as a level-order list with None for
missing children."""


def check(root: list) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree has at least one node"
    nodes = [0]
    pos = 1
    ptr = 0
    while ptr < len(nodes):
        for _ in range(2):
            if pos < len(root):
                if root[pos] is not None:
                    nodes.append(pos)
                pos += 1
        ptr += 1
    assert pos >= len(root), "level-order list describes a valid binary tree"
    assert 1 <= len(nodes) <= 100, "number of nodes in [1, 100]"
    assert all(-100 <= root[i] <= 100 for i in nodes), "-100 <= Node.val <= 100"
