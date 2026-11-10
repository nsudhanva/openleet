"""Most Frequent Subtree Sum at 10^4 nodes: a deep chain or random tree, with values from a
tiny set so many subtree sums tie."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 10**4


def generate(rng):
    left, right = shaped_tree(rng, N, "chain" if rng.random() < 0.4 else "random")
    if rng.random() < 0.5:
        vals = [rng.choice((-1, 0, 1)) for _ in range(N)]
    else:
        vals = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
