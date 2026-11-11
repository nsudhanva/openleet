"""Amount of Time for Binary Tree to Be Infected at 2 * 10^4 nodes: a chain or a thin tree with
the infection starting near the middle, so the spread takes ~10^4 minutes and re-scanning the
tree each minute is ~2 * 10^8 steps."""

from _shapes import level_order, shaped_tree, thin_tree

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        left, right = shaped_tree(rng, N, "chain")
    else:
        left, right = thin_tree(rng, N, 3)
    vals = rng.sample(range(1, 10**5 + 1), N)
    start = vals[rng.randint(N // 3, N // 2)]
    return {"root": level_order(vals, left, right), "start": start}
