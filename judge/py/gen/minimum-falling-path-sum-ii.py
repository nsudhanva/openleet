"""Minimum Falling Path Sum II on a 15 by 15 grid of values in [-99, 99]: trying every
falling path without memoization is 15 * 14^14 ~ 10^17 paths."""

SEEDS = 2
N = 15


def generate(rng):
    return {"grid": [[rng.randint(-99, 99) for _ in range(N)] for _ in range(N)]}
