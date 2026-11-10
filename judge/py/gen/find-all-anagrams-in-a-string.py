"""Find All Anagrams in a String with |s| = 3 * 10^4 and a long p over a small alphabet, so
re-counting each window is quadratic and many windows match."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    alphabet = rng.choice(["ab", "abc", ascii_lowercase])
    s = random_string(rng, alphabet, N)
    plen = rng.choice([1000, 10**4])
    p = random_string(rng, alphabet, plen)
    return {"s": s, "p": p}
