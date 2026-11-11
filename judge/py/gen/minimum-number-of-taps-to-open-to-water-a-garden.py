"""Minimum Number of Taps to Open to Water a Garden at n = 10^4 with ranges of 1 (three in four)
or 2, so ~4000 taps are needed and finding each next tap by scanning all n + 1 taps is
quadratic."""

SEEDS = 2
N = 10**4


def generate(rng):
    return {"n": N, "ranges": [1 if rng.random() < 0.75 else 2 for _ in range(N + 1)]}
