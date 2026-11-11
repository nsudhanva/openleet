"""Longest Subarray of 1's After Deleting One Element at n = 2 * 10^4 with 30-50% zeros, so
deleting each element (or each zero) in turn and rescanning costs ~10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    p = rng.uniform(0.3, 0.5)
    return {"nums": [0 if rng.random() < p else 1 for _ in range(N)]}
