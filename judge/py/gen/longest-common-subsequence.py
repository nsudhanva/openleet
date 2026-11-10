"""Longest Common Subsequence with both strings at length 1000, over a tiny alphabet (long
answer) or the full alphabet."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 1000


def generate(rng):
    alphabet = rng.choice(["ab", "abcd", ascii_lowercase])
    return {
        "text1": random_string(rng, alphabet, N),
        "text2": random_string(rng, alphabet, N),
    }
