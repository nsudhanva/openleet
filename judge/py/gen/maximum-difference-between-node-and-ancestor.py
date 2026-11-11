"""Maximum Difference Between Node and Ancestor at 5000 nodes (the maximum) in a chain, so
comparing every node with each of its descendants is ~1.25 * 10^7 pairs."""

from _shapes import level_order, shaped_tree

SEEDS = 2
N = 5000


def generate(rng):
    left, right = shaped_tree(rng, N, "chain")
    vals = [rng.randint(0, 10**5) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
