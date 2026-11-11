"""Closest Nodes Queries in a BST with 2 * 10^4 nodes and queries: the tree is a chain (sorted
inserts) or a zigzag (inserts alternating from both ends), so walking it per query is ~n deep."""

from _shapes import insert_bst, level_order

SEEDS = 2
N = 2 * 10**4
Q = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    vals = sorted(rng.sample(range(1, LIMIT + 1), N))
    if rng.random() < 0.5:
        order = list(range(N))
        if rng.random() < 0.5:
            order.reverse()
    else:
        lo, hi, order = 0, N - 1, []
        while lo <= hi:
            order.append(lo)
            lo += 1
            if lo <= hi:
                order.append(hi)
                hi -= 1
    left, right = insert_bst(vals, order)
    queries = [rng.choice(vals) if rng.random() < 0.2 else rng.randint(1, LIMIT) for _ in range(Q)]
    return {"root": level_order(vals, left, right, root=order[0]), "queries": queries}
