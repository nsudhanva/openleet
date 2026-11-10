"""Flip Equivalent Binary Trees at the maximum 100 nodes: root2 is root1 with random flips, or
additionally has two values swapped."""

from _shapes import level_order, random_tree, thin_tree

SEEDS = 3
N = 100


def generate(rng):
    left, right = thin_tree(rng, N, 3, -1) if rng.random() < 0.3 else random_tree(rng, N, -1)
    vals = rng.sample(range(100), N)
    root1 = level_order(vals, left, right, empty=-1)
    left2, right2 = left[:], right[:]
    for u in range(N):
        if rng.random() < 0.5:
            left2[u], right2[u] = right2[u], left2[u]
    vals2 = vals[:]
    if rng.random() < 0.34:
        i, j = rng.sample(range(N), 2)
        vals2[i], vals2[j] = vals2[j], vals2[i]
    return {"root1": root1, "root2": level_order(vals2, left2, right2, empty=-1)}
