"""Invert Binary Tree at the maximum 100 nodes, bushy or a deep chain."""

from _shapes import level_order, random_tree, thin_tree

SEEDS = 2
N = 100


def generate(rng):
    left, right = thin_tree(rng, N, 3, -1) if rng.random() < 0.5 else random_tree(rng, N, -1)
    vals = [rng.randint(-100, 100) for _ in range(N)]
    return {"root": level_order(vals, left, right, empty=-1)}
