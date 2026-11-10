"""Shuffle the Array at the maximum n = 500 (1000 values in [1, 10^3])."""

SEEDS = 2


def generate(rng):
    return {"nums": [rng.randint(1, 1000) for _ in range(1000)], "n": 500}
