"""Minimum Operations to Make the Array K-Increasing at n = 1.5 * 10^4 with k = 1 or 2 and random
values, so the quadratic longest non-decreasing subsequence DP over each of the k long chains
costs ~10^8 steps against patience sorting."""

SEEDS = 2
N = 15000


def generate(rng):
    return {"arr": [rng.randint(1, N) for _ in range(N)], "k": rng.randint(1, 2)}
