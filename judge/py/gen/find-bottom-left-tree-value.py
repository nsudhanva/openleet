"""Find Bottom Left Tree Value with 10^4 nodes and full 32-bit values: a random tree, or a
zigzag chain 10^4 deep whose bottom node is on the right side."""

from _shapes import level_order, random_tree, zigzag_path

SEEDS = 2
N = 10**4


def generate(rng):
    vals = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    left, right = zigzag_path(rng, N, -1) if rng.random() < 0.5 else random_tree(rng, N, -1)
    return {"root": level_order(vals, left, right, empty=-1)}
