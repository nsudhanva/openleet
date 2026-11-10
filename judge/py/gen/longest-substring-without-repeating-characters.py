"""Longest Substring Without Repeating Characters at length 10^5 over all 95 printable ASCII
characters (long windows), or a two-letter alphabet."""

from _shapes import random_string

SEEDS = 2
N = 10**5
PRINTABLE = "".join(chr(c) for c in range(32, 127))


def generate(rng):
    alphabet = rng.choice([PRINTABLE, "ab"])
    return {"s": random_string(rng, alphabet, N)}
