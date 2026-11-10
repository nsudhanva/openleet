"""Reverse Only Letters on 100-character strings mixing letters and symbols (no quote or
backslash)."""

from _shapes import random_string

SEEDS = 2
CHARS = [chr(c) for c in range(33, 123) if chr(c) not in '"\\']


def generate(rng):
    return {"s": random_string(rng, CHARS, 100)}
