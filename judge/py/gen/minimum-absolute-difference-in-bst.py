"""Minimum Absolute Difference in BST at 10^4 nodes with distinct values in [0, 10^5]: a
random-shape BST or a fully skewed chain."""

from _shapes import level_order, random_bst

SEEDS = 3
N = 10**4


def generate(rng):
    skew = rng.random() < 0.5
    vals = sorted(rng.sample(range(10**5 + 1), N))
    root, left, right = random_bst(rng, N, "left" if skew else None)
    return {"root": level_order(vals, left, right, root)}
