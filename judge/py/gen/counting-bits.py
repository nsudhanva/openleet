"""Counting Bits at the maximum n = 10^5 (and a nearby value)."""

SEEDS = 2


def generate(rng):
    return {"n": rng.choice([10**5, rng.randint(9 * 10**4, 10**5)])}
