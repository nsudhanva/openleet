"""Average of Levels at 10^4 nodes with values at the 32-bit extremes (level sums overflow 32
bits): a random tree, a deep mostly-chain tree, or a full chain."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 10**4


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    if rng.random() < 0.5:
        vals = [rng.choice([-(2**31), 2**31 - 1]) for _ in range(N)]
    else:
        vals = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
