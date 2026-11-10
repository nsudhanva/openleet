"""Binary Tree Cameras at the maximum 1000 nodes: a chain 1000 deep, a deep mostly-chain tree,
or a random tree."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 1000


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = [0] * N
    return {"root": level_order(vals, left, right)}
