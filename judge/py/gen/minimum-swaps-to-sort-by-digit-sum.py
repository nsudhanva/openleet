"""Minimum Swaps to Sort by Digit Sum at n = 10^5 distinct values in random order, so locating
each element's target by a linear scan is ~5 * 10^9 steps."""

SEEDS = 2
N = 10**5


def generate(rng):
    return {"nums": rng.sample(range(1, 10**9 + 1), N)}
