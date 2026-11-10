"""Weighted Word Mapping at the maximum 100 words of 10 letters with weights up to 100."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    words = [random_string(rng, ascii_lowercase, rng.randint(1, 10)) for _ in range(100)]
    return {"words": words, "weights": [rng.randint(1, 100) for _ in range(26)]}
