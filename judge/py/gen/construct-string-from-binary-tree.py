"""Construct String from Binary Tree with 10^4 nodes: a random tree, or a single zigzag chain
10^4 deep that punishes quadratic string concatenation and shallow recursion."""

from _shapes import level_order, random_tree, zigzag_path

SEEDS = 2
N = 10**4


def generate(rng):
    vals = [rng.randint(-1000, 1000) for _ in range(N)]
    left, right = zigzag_path(rng, N, -1) if rng.random() < 0.5 else random_tree(rng, N, -1)
    return {"root": level_order(vals, left, right, empty=-1)}
