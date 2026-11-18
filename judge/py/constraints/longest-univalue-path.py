"""Longest Univalue Path: a binary tree as a level-order list with None for missing children."""


def check(root: list) -> None:
    assert isinstance(root, list), "root is a level-order list"
    # Build the tree the way level-order lists are read; entries no node reaches are ignored.
    vals = []
    if root and root[0] is not None:
        level, idx, depth = [0], 1, 0
        while level:
            depth += 1
            vals.extend(root[i] for i in level)
            nxt = []
            for _ in level:
                for _ in range(2):
                    if idx < len(root) and root[idx] is not None:
                        nxt.append(idx)
                    idx += 1
            level = nxt
        assert depth <= 1000, "the depth of the tree will not exceed 1000"
    assert 0 <= len(vals) <= 10**4, "the number of nodes is in the range [0, 10^4]"
    assert all(-1000 <= v <= 1000 for v in vals), "-1000 <= Node.val <= 1000"
