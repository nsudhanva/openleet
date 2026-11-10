"""Number of Lines To Write String with the maximum 1000 letters and random widths in [2, 10]."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    widths = [rng.randint(2, 10) for _ in range(26)]
    return {"widths": widths, "s": random_string(rng, ascii_lowercase, 1000)}
