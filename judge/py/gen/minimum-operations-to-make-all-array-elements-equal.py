"""Minimum Operations to Make All Array Elements Equal with 10^4 numbers and 10^4 queries, so
summing the distance to every number for each query costs 10^8 steps against sorting plus prefix
sums and binary search."""

SEEDS = 2
N = 10**4
M = 10**4
LIMIT = 10**9


def generate(rng):
    return {
        "nums": [rng.randint(1, LIMIT) for _ in range(N)],
        "queries": [rng.randint(1, LIMIT) for _ in range(M)],
    }
