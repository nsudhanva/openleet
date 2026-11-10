"""Path Sum on a 5000-node tree: a random shape or a deep, nearly linear one, with the target
set to a real root-to-leaf sum (or one that misses)."""

from _shapes import leaf_sums, level_order, random_tree, skewed_tree

SEEDS = 2
N = 5000


def generate(rng):
    deep = rng.random() < 0.5
    left, right = skewed_tree(rng, N, -1) if deep else random_tree(rng, N, -1)
    vals = [rng.randint(-20, 20) for _ in range(N)]
    sums = [s for s in leaf_sums(vals, left, right, empty=-1) if -1000 <= s <= 1000]
    target = rng.choice(sums) if sums and rng.random() < 0.5 else rng.randint(-1000, 1000)
    return {"root": level_order(vals, left, right, empty=-1), "targetSum": target}
