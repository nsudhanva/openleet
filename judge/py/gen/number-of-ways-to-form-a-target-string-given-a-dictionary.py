"""Number of Ways to Form a Target String Given a Dictionary at 200 words of 300 letters over a
small alphabet and a 150-letter target, so every column can serve every target letter and trying
each choice of columns without a memo explores an exponential number of them."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
WORDS = 200
LENGTH = 300
TARGET = 150


def generate(rng):
    alphabet = rng.sample(ascii_lowercase, rng.randint(3, 8))
    words = [random_string(rng, alphabet, LENGTH) for _ in range(WORDS)]
    return {"words": words, "target": random_string(rng, alphabet, TARGET)}
