"""Shortest Common Supersequence on two 1000-letter strings over a small alphabet (O(n * m) DP
of 10^6 cells)."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alphabet = rng.choice(["ab", "abcd", ascii_lowercase])
    return {
        "str1": random_string(rng, alphabet, 1000),
        "str2": random_string(rng, alphabet, 1000),
    }
