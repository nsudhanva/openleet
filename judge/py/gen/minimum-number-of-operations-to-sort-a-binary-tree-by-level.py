"""Minimum Number of Operations to Sort a Binary Tree by Level on a heap-shaped complete tree of
10^5 nodes holding a shuffled permutation of 1..10^5, so an O(w^2) sort or lookup per level is
quadratic on the 34465-node bottom level."""

from _shapes import level_order

SEEDS = 2
N = 10**5


def generate(rng):
    left = [2 * i + 1 if 2 * i + 1 < N else None for i in range(N)]
    right = [2 * i + 2 if 2 * i + 2 < N else None for i in range(N)]
    vals = rng.sample(range(1, N + 1), N)
    return {"root": level_order(vals, left, right)}
