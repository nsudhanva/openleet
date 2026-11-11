"""Two Sum BSTs at 5000 nodes per tree, both degenerate chains, with a target no pair reaches
and above every value of the second tree, so searching that tree for each value of the first
walks its whole chain: ~2.5 * 10^7 steps."""

from _shapes import insert_bst, level_order

SEEDS = 2
N = 5000
TOP = 10**9


def generate(rng):
    # Even values and an odd target, so no pair sums to it; target - a > 0 > every b.
    a = [2 * v for v in rng.sample(range(-TOP // 4, 0), N)]
    b = [2 * v for v in rng.sample(range(-TOP // 2, -TOP // 4), N)]
    a.sort(reverse=rng.random() < 0.5)
    b.sort()
    trees = []
    for values in (a, b):
        left, right = insert_bst(values, range(N))
        trees.append(level_order(values, left, right))
    target = 2 * rng.randrange(TOP // 4) + 1
    return {"root1": trees[0], "root2": trees[1], "target": target}
