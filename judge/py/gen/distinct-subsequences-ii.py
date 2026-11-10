"""Distinct Subsequences II at length 2000: random letters, or a tiny alphabet with many
repeats so duplicate subsequences must be subtracted."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
L = 2000


def generate(rng):
    alphabet = ascii_lowercase if rng.random() < 0.5 else "ab"
    return {"s": random_string(rng, alphabet, L)}
