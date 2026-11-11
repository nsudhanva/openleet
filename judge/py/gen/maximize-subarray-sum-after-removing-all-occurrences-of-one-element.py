"""Maximize Subarray Sum After Removing All Occurrences of One Element at n = 2 * 10^4 drawn from
5000 distinct values, so rerunning Kadane once per value removed is 10^8 steps."""

SEEDS = 2
N = 2 * 10**4
DISTINCT = 5000
TOP = 10**6


def generate(rng):
    pool = rng.sample(range(-TOP, TOP + 1), DISTINCT)
    return {"nums": [rng.choice(pool) for _ in range(N)]}
