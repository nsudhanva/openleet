"""Squares of a Sorted Array at n = 10^4 sorted values spanning negatives and positives."""

SEEDS = 3


def generate(rng):
    lo, hi = rng.choice([(-(10**4), 10**4), (-(10**4), 0), (-5, 10**4)])
    return {"nums": sorted(rng.randint(lo, hi) for _ in range(10**4))}
