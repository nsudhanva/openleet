"""Lowest Common Ancestor of a binary tree: a level-order tree and two node values p and q."""


def check(root: list, p: int, q: int) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "the tree has a root"
    # Build the tree the way level-order lists are read; entries no node reaches are ignored.
    n = len(root)
    left = [None] * n
    right = [None] * n
    order = [0]
    idx = 1
    for par in order:
        for side in (left, right):
            if idx < n and root[idx] is not None:
                side[par] = idx
                order.append(idx)
            idx += 1
    vals = [root[i] for i in order]
    assert 2 <= len(vals) <= 10**5, "the number of nodes is in the range [2, 10^5]"
    assert all(-(10**9) <= v <= 10**9 for v in vals), "-10^9 <= Node.val <= 10^9"
    assert len(set(vals)) == len(vals), "all Node.val are unique"
    assert p != q, "p != q"
    assert p in set(vals) and q in set(vals), "p and q will exist in the tree"
