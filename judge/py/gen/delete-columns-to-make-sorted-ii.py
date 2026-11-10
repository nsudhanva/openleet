"""Delete Columns to Make Sorted II with 100 strings of length 100 sharing long common
prefixes, so ties persist across many kept columns."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N, L = 100, 100


def generate(rng):
    alphabet = ascii_lowercase if rng.random() < 0.5 else "ab"
    strs = [random_string(rng, alphabet, L) for _ in range(N)]
    return {"strs": strs}
