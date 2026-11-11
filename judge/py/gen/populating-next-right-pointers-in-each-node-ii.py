"""Populating Next Right Pointers II at the maximum 6000 nodes on a tree thousands of levels
deep with ragged levels, so one walk of the tree per level is ~2 * 10^7 steps and next pointers
must skip long gaps."""

from _shapes import level_order, skewed_tree, thin_tree

SEEDS = 2
N = 6000


def generate(rng):
    left, right = skewed_tree(rng, N, rate=0.5) if rng.random() < 0.5 else thin_tree(rng, N, 4)
    vals = [rng.randint(-100, 100) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
