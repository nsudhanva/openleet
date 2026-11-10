"""Non-overlapping Palindrome Substrings at length 2000 (cubic palindrome checks time out):
one repeated letter, or a two-letter alphabet, with k small or large."""

from _shapes import random_string

SEEDS = 3
N = 2000


def generate(rng):
    alphabet = rng.choice(["a", "ab", "abc"])
    s = random_string(rng, alphabet, N)
    k = rng.choice([1, rng.randint(2, 20), rng.randint(1, N)])
    return {"s": s, "k": k}
