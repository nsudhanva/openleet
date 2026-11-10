"""Lowest Common Ancestor in a BST of 10^5 unique values: a random-insertion BST, or a long
chain (one path 10^5 deep) with p and q near the bottom."""

from _shapes import insert_bst, level_order

SEEDS = 2
N = 10**5
LIMIT = 10**9


def generate(rng):
    vals = sorted(rng.sample(range(-LIMIT, LIMIT + 1), N))
    if rng.random() < 0.5:
        # Zigzag chain: take values from both ends, each node the only child of the last.
        lo, hi = 0, N - 1
        order = []
        while lo <= hi:
            if rng.random() < 0.5:
                order.append(lo)
                lo += 1
            else:
                order.append(hi)
                hi -= 1
        p, q = rng.sample(order[-50:], 2)
    else:
        order = list(range(N))
        rng.shuffle(order)
        p, q = rng.sample(range(N), 2)
    left, right = insert_bst(vals, order)
    return {"root": level_order(vals, left, right, order[0]), "p": vals[p], "q": vals[q]}
