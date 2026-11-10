"""Trim a BST at 10^4 nodes: a fully degenerate chain (deep recursion) or a random insertion
BST, with low/high cutting through the middle."""

from _shapes import insert_bst, level_order, pick_shape

SEEDS = 3
N = 10**4
TOP = 10**4


def generate(rng):
    shape = pick_shape(rng)
    values = rng.sample(range(TOP + 1), N)
    if shape == 0:
        values.sort()
    elif shape == 1:
        values.sort(reverse=True)
    left, right = insert_bst(values, range(N))
    a, b = rng.randint(0, TOP), rng.randint(0, TOP)
    return {"root": level_order(values, left, right), "low": min(a, b), "high": max(a, b)}
