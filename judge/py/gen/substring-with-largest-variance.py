"""Substring With Largest Variance at n = 10^4 over all 26 letters, skewed so a few dominate,
so counting letters over every substring is ~5 * 10^7 steps of a 26-way max and min."""

from string import ascii_lowercase

SEEDS = 2
N = 10**4


def generate(rng):
    weights = [rng.random() ** 3 for _ in ascii_lowercase]
    return {"s": "".join(rng.choices(ascii_lowercase, weights, k=N))}
