"""Minimum ASCII Delete Sum at 1000 x 1000 characters: a small alphabet so the strings share
long subsequences, or the full alphabet."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 3
N = 1000


def generate(rng):
    alphabet = rng.choice(("ab", "abcd", ascii_lowercase))
    return {
        "s1": random_string(rng, alphabet, N),
        "s2": random_string(rng, alphabet, N),
    }
