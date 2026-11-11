"""Binary Tree Tilt at 10^4 nodes as a chain or a thin tree ~7500 levels deep, so recomputing
each node's subtree sums from scratch costs over 2.5 * 10^7 visits."""

from _shapes import level_order, thin_tree, zigzag_path

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        left, right = zigzag_path(rng, N)
    else:
        left, right = thin_tree(rng, N, 3)
    vals = [rng.randint(-1000, 1000) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
