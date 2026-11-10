"""Path Sum II on a 5000-node tree: a random shape with values mostly zero so many root-to-leaf
paths hit the target, or a deep, nearly linear tree."""

from _shapes import leaf_sums, level_order, random_tree, skewed_tree

SEEDS = 2
N = 5000


def generate(rng):
    deep = rng.random() < 0.5
    left, right = skewed_tree(rng, N, -1) if deep else random_tree(rng, N, -1)
    vals = [0 if rng.random() < 0.7 else rng.randint(-3, 3) for _ in range(N)]
    sums = sorted(s for s in leaf_sums(vals, left, right, empty=-1) if -1000 <= s <= 1000)
    target = sums[len(sums) // 2] if sums else 0
    return {"root": level_order(vals, left, right, empty=-1), "targetSum": target}
