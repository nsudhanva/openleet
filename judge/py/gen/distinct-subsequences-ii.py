"""Distinct Subsequences II at length 2000: random letters, or a tiny alphabet with many
repeats so duplicate subsequences must be subtracted."""

from _shapes import random_string

SEEDS = 2
L = 2000


def generate(rng):
    alphabet = "abcdefghijklmnopqrstuvwxyz" if rng.random() < 0.5 else "ab"
    return {"s": random_string(rng, alphabet, L)}
