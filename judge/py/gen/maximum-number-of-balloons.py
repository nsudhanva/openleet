"""Maximum Number of Balloons on 10^4 letters drawn mostly from "balon" with skewed counts."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 10**4


def generate(rng):
    alphabet = "balloon" * 3 + "xyz" if rng.random() < 0.5 else ascii_lowercase
    return {"text": random_string(rng, alphabet, N)}
