"""Convert BST to Greater Tree with 10^4 unique values: a random-insertion BST, or a
degenerate chain 10^4 deep (sorted insertion order)."""

from _shapes import insert_bst, level_order

SEEDS = 2
N = 10**4


def generate(rng):
    vals = rng.sample(range(-(10**4), 10**4 + 1), N)
    if rng.random() < 0.5:
        vals.sort(reverse=rng.random() < 0.5)
    left, right = insert_bst(vals, range(N))
    return {"root": level_order(vals, left, right)}
