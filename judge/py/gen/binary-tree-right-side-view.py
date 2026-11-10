"""Binary Tree Right Side View at the maximum 100 nodes: a zigzag chain where the visible node
switches sides, a deep mostly-chain tree, or a random tree."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 100


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = [rng.randint(-100, 100) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
