"""Binary Tree Tilt at 10^4 nodes: a chain 10^4 deep (recursion and repeated-subtree-sum worst
case), a deep mostly-chain tree, or a random tree."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 10000


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = [rng.randint(-1000, 1000) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
