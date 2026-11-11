"""Split Message Based on Limit with a 10^4-character message and limit 12, which takes 8,893
parts, so recomputing each part count's capacity from scratch is ~4 * 10^7 steps."""

from _shapes import random_string

SEEDS = 2
N = 10**4
LIMIT = 12


def generate(rng):
    alphabet = "abcdefghij " if rng.random() < 0.5 else "xyz "
    return {"message": random_string(rng, alphabet, N), "limit": LIMIT}
