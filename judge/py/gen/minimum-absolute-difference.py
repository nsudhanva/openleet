"""Minimum Absolute Difference at n = 2 * 10^4 distinct values, so comparing every pair is
2 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    return {"arr": rng.sample(range(-LIMIT, LIMIT + 1), N)}
