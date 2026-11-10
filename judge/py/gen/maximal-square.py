"""Maximal Square on a 300 x 300 binary matrix: all ones but a few zeros (the square grows
huge, expanding from every cell is quartic), or random cells."""

SEEDS = 2
N = 300


def generate(rng):
    p = rng.choice([0.9995, 0.7])
    return {"matrix": [["1" if rng.random() < p else "0" for _ in range(N)] for _ in range(N)]}
