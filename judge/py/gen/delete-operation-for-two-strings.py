"""Delete Operation for Two Strings at 500 x 500: random letters, or a small alphabet so the
LCS is long and memoized recursion goes deep."""

from _shapes import random_string

SEEDS = 2
L = 500
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    alphabet = LETTERS if rng.random() < 0.5 else "ab"
    word1 = random_string(rng, alphabet, L)
    word2 = random_string(rng, alphabet, L)
    return {"word1": word1, "word2": word2}
