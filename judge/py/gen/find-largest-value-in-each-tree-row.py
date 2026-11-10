"""Largest Value in Each Tree Row with 10^4 nodes over the full 32-bit range: a bushy random tree
or a deep, narrow one."""

from _shapes import level_order, random_tree, thin_tree

SEEDS = 2
N = 10**4


def generate(rng):
    left, right = thin_tree(rng, N, 3, -1) if rng.random() < 0.5 else random_tree(rng, N, -1)
    vals = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    return {"root": level_order(vals, left, right, empty=-1)}
