"""Longest Increasing Subsequence at n = 2500, values in [-10^4, 10^4]."""

SEEDS = 2


def generate(rng):
    return {"nums": [rng.randint(-(10**4), 10**4) for _ in range(2500)]}
