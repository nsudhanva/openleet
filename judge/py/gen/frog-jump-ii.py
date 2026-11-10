"""Frog Jump II with 10^5 strictly increasing stones up to 10^9."""

SEEDS = 2
N = 10**5


def generate(rng):
    hi = rng.choice([2 * 10**5, 10**9])
    return {"stones": [0, *sorted(rng.sample(range(1, hi + 1), N - 1))]}
