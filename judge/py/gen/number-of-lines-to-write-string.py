"""Number of Lines To Write String with the maximum 1000 letters and random widths in [2, 10]."""

from _shapes import random_string

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    widths = [rng.randint(2, 10) for _ in range(26)]
    return {"widths": widths, "s": random_string(rng, LETTERS, 1000)}
