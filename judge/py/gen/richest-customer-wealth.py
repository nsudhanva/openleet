"""Richest Customer Wealth on a full 50 x 50 grid of values in [1, 100]."""

SEEDS = 2


def generate(rng):
    return {"accounts": [[rng.randint(1, 100) for _ in range(50)] for _ in range(50)]}
