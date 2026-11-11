"""Split Concatenated Strings with 50 strings of 20 letters from a two-letter alphabet (1,000
letters in all), so trying every reversal choice is 2^50 loops."""

from _shapes import random_string

SEEDS = 2
COUNT = 50
LENGTH = 20


def generate(rng):
    alphabet = "ab" if rng.random() < 0.5 else "zy"
    return {"strs": [random_string(rng, alphabet, LENGTH) for _ in range(COUNT)]}
