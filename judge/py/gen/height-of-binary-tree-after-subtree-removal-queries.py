"""Height of Binary Tree After Subtree Removal Queries at n = m = 5000: a chain, a deep
mostly-chain tree or a random tree, so re-measuring the height for each query costs
~2.5 * 10^7 node visits."""

from _shapes import level_order, pick_shape, shaped_tree

SEEDS = 3
N = 5000
M = 5000


def generate(rng):
    kind = ("chain", "deep", "random")[pick_shape(rng)]
    left, right = shaped_tree(rng, N, kind)
    vals = list(range(1, N + 1))
    rng.shuffle(vals)
    queries = [vals[rng.randrange(1, N)] for _ in range(M)]
    return {"root": level_order(vals, left, right), "queries": queries}
