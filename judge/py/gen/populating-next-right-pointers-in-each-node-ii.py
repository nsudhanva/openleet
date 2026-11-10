"""Populating Next Right Pointers II on a 6000-node tree: a random shape with ragged levels,
or a deep sparse one where next pointers must skip long gaps."""

from _shapes import level_order, random_tree, skewed_tree

SEEDS = 2
N = 6000


def generate(rng):
    left, right = skewed_tree(rng, N, rate=0.5) if rng.random() < 0.5 else random_tree(rng, N)
    vals = [rng.randint(-100, 100) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
