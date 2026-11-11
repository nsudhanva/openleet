"""Strobogrammatic Number III with high at 9 digits (or 12) and low a few digits shorter, so
testing every number in the range is 10^9 or more checks against at most ~10^5 generated
candidates."""

SEEDS = 2


def generate(rng):
    digits = 9 if rng.random() < 0.5 else 12
    high = rng.randrange(10 ** (digits - 1), 10**digits)
    low = rng.randrange(0, 10 ** (digits - 6))
    return {"low": str(low), "high": str(high)}
