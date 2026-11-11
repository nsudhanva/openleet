"""Count Pairs of Equal Substrings With Minimum Difference at two strings of length 2 * 10^5,
the second ending with the permutation of the alphabet the first starts with (26 tied
quadruples), so pairing every position of one with every same-letter position of the other
costs ~1.5 * 10^9 steps."""

from _shapes import random_string

SEEDS = 2
N = 2 * 10**5
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    perm = "".join(rng.sample(ALPHABET, len(ALPHABET)))
    first = perm + random_string(rng, ALPHABET, N - len(perm))
    second = random_string(rng, ALPHABET, N - len(perm)) + perm
    return {"firstString": first, "secondString": second}
