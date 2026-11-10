"""Longest Palindromic Subsequence at length 1000 (exponential without DP), over a tiny or
full alphabet."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alphabet = rng.choice(["ab", ascii_lowercase])
    return {"s": random_string(rng, alphabet, 1000)}
