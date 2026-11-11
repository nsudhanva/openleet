"""Pairs of Songs at the maximum 6 * 10^4 durations in [1, 500], so checking every pair does
~1.8 * 10^9 sums."""

SEEDS = 2
N = 6 * 10**4


def generate(rng):
    return {"time": [rng.randint(1, 500) for _ in range(N)]}
