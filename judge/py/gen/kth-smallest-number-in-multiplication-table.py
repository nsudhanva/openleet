"""Kth Smallest in a Multiplication Table with m, n near 3 * 10^4 (up to 9 * 10^8 cells),
too many to enumerate."""

SEEDS = 2
LIMIT = 3 * 10**4


def generate(rng):
    m = rng.randint(LIMIT - 1000, LIMIT)
    n = rng.randint(LIMIT - 1000, LIMIT)
    return {"m": m, "n": n, "k": rng.randint(1, m * n)}
