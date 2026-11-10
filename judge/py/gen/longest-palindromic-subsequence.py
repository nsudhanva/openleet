"""Longest Palindromic Subsequence at length 1000 (exponential without DP), over a tiny or
full alphabet."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alphabet = rng.choice(["ab", "abcdefghijklmnopqrstuvwxyz"])
    return {"s": random_string(rng, alphabet, 1000)}
