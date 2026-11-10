"""Reveal Cards with the maximum deck of 1000 distinct values in [1, 10^6]."""

SEEDS = 2


def generate(rng):
    return {"deck": rng.sample(range(1, 10**6 + 1), 1000)}
