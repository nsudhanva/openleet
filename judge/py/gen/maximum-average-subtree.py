"""Maximum Average Subtree at 10^4 nodes in a chain (each child on a random side), so summing
every subtree from scratch is ~5 * 10^7 node visits."""

from _shapes import level_order, shaped_tree

SEEDS = 2
N = 10**4


def generate(rng):
    left, right = shaped_tree(rng, N, "chain")
    vals = [rng.randint(0, 10**5) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
