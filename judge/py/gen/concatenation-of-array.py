"""Concatenation of Array at the maximum length 1000 with random values."""

SEEDS = 2


def generate(rng):
    return {"nums": [rng.randint(1, 1000) for _ in range(1000)]}
