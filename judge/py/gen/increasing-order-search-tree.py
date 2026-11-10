"""Increasing Order Search Tree at the maximum 100 nodes, a random or left-deep BST with unique
values in [0, 1000]."""

from _shapes import inorder, level_order, random_tree, thin_tree

SEEDS = 3
N = 100


def generate(rng):
    shape = rng.randrange(3)
    if shape == 2:
        left, right = [*range(1, N), -1], [-1] * N
    else:
        left, right = thin_tree(rng, N, 3, -1) if shape == 1 else random_tree(rng, N, -1)
    vals = [0] * N
    for node, v in zip(
        inorder(left, right, empty=-1), sorted(rng.sample(range(1001), N)), strict=False
    ):
        vals[node] = v
    return {"root": level_order(vals, left, right, empty=-1)}
