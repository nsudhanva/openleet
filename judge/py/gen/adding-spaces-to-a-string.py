"""Adding Spaces at |s| = 3 * 10^5 with 1.1 * 10^5 spaces packed into the first 1.3 * 10^5
characters, so each insertion (string rebuild or bytearray insert) moves nearly the whole string."""

from string import ascii_letters

from _shapes import random_string

SEEDS = 2
N = 3 * 10**5
M = 11 * 10**4
FRONT = 13 * 10**4


def generate(rng):
    s = random_string(rng, ascii_letters, N)
    return {"s": s, "spaces": sorted(rng.sample(range(min(FRONT, N)), M))}
