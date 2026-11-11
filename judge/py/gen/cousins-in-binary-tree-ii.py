"""Cousins in Binary Tree II at 5 * 10^4 nodes in a random (bushy) tree with levels thousands of
nodes wide, so summing each node's cousins by scanning its level costs ~10^8 steps."""

from _shapes import level_order, random_tree

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    left, right = random_tree(rng, N)
    vals = [rng.randint(1, 10**4) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
