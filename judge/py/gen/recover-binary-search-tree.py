"""Recover BST at 1000 nodes with full 32-bit values: a random or deep BST with two swapped
values, either far apart or adjacent in sorted order."""

from _shapes import insert_bst, level_order

SEEDS = 3
N = 1000


def generate(rng):
    vals = rng.sample(range(-(2**31), 2**31), N)
    if rng.random() < 0.5:
        order = list(range(N))
    else:
        # Nearly sorted insertion order gives a deep, path-like tree.
        order = sorted(range(N), key=lambda i: vals[i])
        for _ in range(N // 20):
            i = rng.randrange(N - 1)
            order[i], order[i + 1] = order[i + 1], order[i]
    left, right = insert_bst(vals, order)
    by_val = sorted(range(N), key=lambda i: vals[i])
    if rng.random() < 0.5:
        k = rng.randrange(N - 1)
        a, b = by_val[k], by_val[k + 1]
    else:
        a, b = rng.sample(range(N), 2)
    vals[a], vals[b] = vals[b], vals[a]
    return {"root": level_order(vals, left, right, order[0])}
