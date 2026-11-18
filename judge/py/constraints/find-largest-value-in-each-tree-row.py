"""Find Largest Value in Each Tree Row: a binary tree as a level-order list with None for
missing children."""


def check(root: list) -> None:
    assert len(root) == 0 or root[0] is not None, "root is None or the first entry is a node"
    nodes = [0] if root else []
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
    assert len(nodes) <= 10**4, "number of nodes in [0, 10^4]"
    assert all(-(2**31) <= root[i] <= 2**31 - 1 for i in nodes), "-2^31 <= Node.val <= 2^31 - 1"
