"""Longest Repeating Character Replacement at length 10^5 with varied k, over a small or the
full uppercase alphabet."""

from _shapes import random_string

SEEDS = 3
N = 10**5


def generate(rng):
    alphabet = rng.choice(["AB", "ABCD", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    s = random_string(rng, alphabet, N)
    return {"s": s, "k": rng.choice([0, rng.randint(1, 100), rng.randint(0, N)])}
