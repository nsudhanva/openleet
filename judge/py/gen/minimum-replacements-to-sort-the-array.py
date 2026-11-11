"""Minimum Replacements to Sort the Array at n = 1000 random values up to 10^9 ending in a value of
at most 1000, so finding each split count by trying k = 1, 2, ... costs ~10^6 tries per element
against one division."""

SEEDS = 2
N = 1000
LIMIT = 10**9
LAST = 1000


def generate(rng):
    nums = [rng.randint(1, LIMIT) for _ in range(N - 1)]
    return {"nums": [*nums, rng.randint(1, LAST)]}
