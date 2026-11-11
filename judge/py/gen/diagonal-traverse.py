"""Diagonal Traverse with m * n = 10^4 as a single column or a single row, so scanning every row
(or every column) for each of the m + n - 1 diagonals does ~10^8 steps."""

from _shapes import pick_shape

SEEDS = 2
N = 10**4


def generate(rng):
    m, n = (N, 1) if pick_shape(rng) == 0 else (1, N)
    return {"mat": [[rng.randint(-(10**5), 10**5) for _ in range(n)] for _ in range(m)]}
