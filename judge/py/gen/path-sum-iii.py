"""Path Sum III on a 1000-node tree: small values with many zeros so a huge number of downward
paths match, or a deep, nearly linear tree that makes the O(n^2) scan pay full price."""

from _shapes import level_order, random_tree, skewed_tree

SEEDS = 2
N = 1000


def generate(rng):
    deep = rng.random() < 0.5
    left, right = skewed_tree(rng, N, -1) if deep else random_tree(rng, N, -1)
    if rng.random() < 0.5:
        vals = [0 if rng.random() < 0.5 else rng.randint(-5, 5) for _ in range(N)]
        target = rng.randint(-3, 3)
    else:
        vals = [rng.randint(-(10**9), 10**9) for _ in range(N)]
        target = rng.randint(-1000, 1000)
    return {"root": level_order(vals, left, right, empty=-1), "targetSum": target}
