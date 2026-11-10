"""Balanced Binary Tree at 5000 nodes: a perfectly balanced tree (true, full traversal), a
chain 5000 deep (recursion-depth worst case), or a random tree."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 5000


def _balanced(n):
    left, right = [None] * n, [None] * n
    # Each index range [lo, hi) becomes a subtree rooted at its midpoint; ids follow creation.
    stack, nxt = [(0, n, None, 0)], 0
    while stack:
        lo, hi, parent, side = stack.pop()
        if lo >= hi:
            continue
        me = nxt
        nxt += 1
        if parent is not None:
            (left, right)[side][parent] = me
        mid = (lo + hi) // 2
        stack.append((lo, mid, me, 0))
        stack.append((mid + 1, hi, me, 1))
    return left, right


def generate(rng):
    shape = rng.choice(["balanced", "chain", "random"])
    left, right = _balanced(N) if shape == "balanced" else shaped_tree(rng, N, shape)
    vals = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
