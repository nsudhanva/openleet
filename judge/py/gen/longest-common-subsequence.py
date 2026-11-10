"""Longest Common Subsequence with both strings at length 1000, over a tiny alphabet (long
answer) or the full alphabet."""

from _shapes import random_string

SEEDS = 2
N = 1000


def generate(rng):
    alphabet = rng.choice(["ab", "abcd", "abcdefghijklmnopqrstuvwxyz"])
    return {
        "text1": random_string(rng, alphabet, N),
        "text2": random_string(rng, alphabet, N),
    }
