"""House Robber III with 10^4 nodes (values up to 10^4) in a bushy or a deep, nearly linear tree,
which punishes the exponential recursion without memoization."""

from _shapes import level_order, random_tree, thin_tree

SEEDS = 3
N = 10**4


def generate(rng):
    left, right = thin_tree(rng, N, 3, -1) if rng.random() < 0.5 else random_tree(rng, N, -1)
    vals = [rng.randint(0, 10**4) for _ in range(N)]
    return {"root": level_order(vals, left, right, empty=-1)}
