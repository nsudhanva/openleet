"""Minimum Depth of Binary Tree at 10^5 nodes: a single chain (answer n, deep recursion) or a
random tree with one shallow leaf hidden among deep ones."""

from _shapes import level_order, random_tree, zigzag_path

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        right, left = zigzag_path(rng, N)
    else:
        left, right = random_tree(rng, N)
    vals = [rng.randint(-1000, 1000) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
