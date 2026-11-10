"""Vertical Order Traversal at the maximum 1000 nodes with few distinct values, so many nodes
share a (row, column) and the value tie-break matters; random or zigzag shapes."""

from _shapes import level_order, random_tree

SEEDS = 3
N = 1000


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        left, right = random_tree(rng, N)
    else:
        # Zigzag spine (left, right, left, ...) with a leaf hanging off each spine node.
        left, right = [None] * N, [None] * N
        v, spine, side = 1, 0, 0
        while v < N:
            (left if side == 0 else right)[spine] = v
            nxt = v
            v += 1
            if v < N:
                (right if side == 0 else left)[spine] = v
                v += 1
            spine, side = nxt, 1 - side
    hi = 3 if shape != 2 else 1000
    vals = [rng.randint(0, hi) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
