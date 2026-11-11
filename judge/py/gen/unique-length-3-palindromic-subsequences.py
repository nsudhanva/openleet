"""Unique Length-3 Palindromic Subsequences at 2 * 10^4 random letters, so intersecting the
letters left and right of every middle is ~4 * 10^8 steps."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"s": random_string(rng, ascii_lowercase, N)}
