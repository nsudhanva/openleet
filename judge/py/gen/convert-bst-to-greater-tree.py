"""Convert BST to Greater Tree at the maximum 10^4 unique values inserted in sorted order, a
chain 10^4 deep, so summing the greater values separately for each node costs ~10^8 steps."""

from _shapes import insert_bst, level_order

SEEDS = 2
N = 10**4


def generate(rng):
    vals = sorted(rng.sample(range(-(10**4), 10**4 + 1), N), reverse=rng.random() < 0.5)
    left, right = insert_bst(vals, range(N))
    return {"root": level_order(vals, left, right)}
