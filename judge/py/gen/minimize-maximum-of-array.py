"""Minimize Maximum of Array at n = 8 * 10^4 with large random values, so recomputing each prefix
sum from scratch is quadratic even with C-level slice sums."""

SEEDS = 2
N = 8 * 10**4
LIMIT = 10**9


def generate(rng):
    return {"nums": [rng.randint(0, LIMIT) for _ in range(N)]}
