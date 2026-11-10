"""Flatten Binary Tree with the maximum 2000 nodes, bushy or a deep left-leaning chain."""

from _shapes import level_order, random_tree, thin_tree

SEEDS = 3
N = 2000


def generate(rng):
    shape = rng.randrange(3)
    vals = [rng.randint(-100, 100) for _ in range(N)]
    if shape == 2:
        left = [*list(range(1, N)), -1]
        right = [-1] * N
    else:
        left, right = thin_tree(rng, N, 3, -1) if shape == 1 else random_tree(rng, N, -1)
    return {"root": level_order(vals, left, right, empty=-1)}
