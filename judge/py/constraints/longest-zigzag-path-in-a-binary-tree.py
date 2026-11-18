"""Longest ZigZag Path in a Binary Tree: a binary tree as a level-order list."""


def check(root: list) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "the tree has a root"
    # Build the tree the way level-order lists are read; entries no node reaches are ignored.
    vals = []
    level, idx = [0], 1
    while level:
        vals.extend(root[i] for i in level)
        nxt = []
        for _ in level:
            for _ in range(2):
                if idx < len(root) and root[idx] is not None:
                    nxt.append(idx)
                idx += 1
        level = nxt
    assert 1 <= len(vals) <= 5 * 10**4, "the number of nodes is in the range [1, 5 * 10^4]"
    assert all(1 <= v <= 100 for v in vals), "1 <= Node.val <= 100"
