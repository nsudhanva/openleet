"""Partition String at the maximum 10^5 random lowercase letters, which split into ~3 * 10^4
short segments, so checking each candidate against a list of the segments so far does ~10^9
comparisons."""

from _shapes import random_string

SEEDS = 2
N = 10**5


def generate(rng):
    alphabet = "abcdefghijklmnopqrstuvwxyz"[: rng.choice([20, 26])]
    return {"s": random_string(rng, alphabet, N)}
