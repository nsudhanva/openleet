"""Reverse Degree on a 1000-letter random lowercase string."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    return {"s": random_string(rng, ascii_lowercase, 1000)}
