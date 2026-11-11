"""Using a Robot to Print the Lexicographically Smallest String at 5 * 10^4 random letters
(finding the smallest remaining letter by scanning is ~1.2 * 10^9 steps), or at 10^5 random
letters from just two (re-finding it only when the current one is the smallest still costs a
scan of the rest of the string for half of the letters, ~2.5 * 10^9 steps)."""

from string import ascii_lowercase

from _shapes import pick_shape, random_string

SEEDS = 2
N = 5 * 10**4
BIG = 10**5


def generate(rng):
    if pick_shape(rng) == 0:
        return {"s": random_string(rng, ascii_lowercase, N)}
    return {"s": random_string(rng, "ab", BIG)}
