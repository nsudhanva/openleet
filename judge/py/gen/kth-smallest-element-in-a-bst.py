"""Kth Smallest in a BST with 10^4 distinct values: a right-leaning chain 10^4 deep (k near
n) or a random-insertion BST."""

from _shapes import insert_bst, level_order

SEEDS = 2
N = 10**4


def generate(rng):
    vals = sorted(rng.sample(range(10**4 + 1), N))
    order = list(range(N))
    if rng.random() < 0.5:
        k = rng.randint(N - 100, N)
    else:
        rng.shuffle(order)
        k = rng.randint(1, N)
    left, right = insert_bst(vals, order)
    return {"root": level_order(vals, left, right, order[0]), "k": k}
