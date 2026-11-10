"""Merge Two Binary Trees with 2000 nodes each: random shapes, or two opposite-leaning
chains that overlap only at the root (deep recursion, maximal union)."""

from _shapes import level_order, random_tree

SEEDS = 3
N = 2000
LIMIT = 10**4


def tree(rng, lean):
    """Level-order list of a random tree, or with lean 0 / 1 a left / right chain."""
    if lean is None:
        left, right = random_tree(rng, N)
    else:
        chain, empty = [*range(1, N), None], [None] * N
        left, right = (chain, empty) if lean == 0 else (empty, chain)
    vals = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    return level_order(vals, left, right)


def generate(rng):
    if rng.random() < 0.5:
        return {"root1": tree(rng, None), "root2": tree(rng, None)}
    return {"root1": tree(rng, 0), "root2": tree(rng, 1)}
