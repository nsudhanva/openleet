"""Binary Tree Pruning at the maximum 200 nodes of 0s and 1s: a chain, a deep mostly-chain tree,
or a random tree."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 200


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = [rng.randint(0, 1) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
