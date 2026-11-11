"""Average of Levels at 10^4 nodes with values at the 32-bit extremes (level sums overflow 32
bits), as a chain or a thin tree ~7500 levels deep, so collecting each level by a fresh walk
from the root costs over 2.5 * 10^7 visits."""

from _shapes import level_order, thin_tree, zigzag_path

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        left, right = zigzag_path(rng, N)
    else:
        left, right = thin_tree(rng, N, 3)
    if rng.random() < 0.5:
        vals = [rng.choice([-(2**31), 2**31 - 1]) for _ in range(N)]
    else:
        vals = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
