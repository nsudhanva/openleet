"""Minimum ASCII Delete Sum at 1000 x 1000 characters: a small alphabet so the strings share
long subsequences, or the full alphabet."""

from _shapes import random_string

SEEDS = 3


def generate(rng):
    alphabet = rng.choice(("ab", "abcd", "abcdefghijklmnopqrstuvwxyz"))
    return {
        "s1": random_string(rng, alphabet, 1000),
        "s2": random_string(rng, alphabet, 1000),
    }
