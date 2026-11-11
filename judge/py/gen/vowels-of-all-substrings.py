"""Vowels of All Substrings at 2 * 10^4 random letters, so counting the vowels of every
substring is ~2 * 10^8 steps."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"word": random_string(rng, ascii_lowercase, N)}
