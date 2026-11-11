"""Using a Robot to Print the Lexicographically Smallest String at 5 * 10^4 random letters,
so finding the smallest remaining letter by scanning is ~1.2 * 10^9 steps."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    return {"s": random_string(rng, ascii_lowercase, N)}
