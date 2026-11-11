"""Maximum Difference Between Node and Ancestor on 8 chains of 5000 nodes (the maximum), so
comparing every node with each of its ancestors is ~10^8 pairs in all."""

from _shapes import level_order, shaped_tree

SEEDS = 8
N = 5000


def generate(rng):
    left, right = shaped_tree(rng, N, "chain")
    vals = [rng.randint(0, 10**5) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
