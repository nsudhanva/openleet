"""Palindrome Partitioning II at length 2000: nearly all one letter (palindromes everywhere),
or random over two letters, both forcing the full O(n^2) DP."""

from _shapes import random_string

SEEDS = 2
N = 2000


def generate(rng):
    if rng.random() < 0.5:
        s = ["a"] * N
        for _ in range(rng.randint(1, 5)):
            s[rng.randrange(N)] = "b"
        s = "".join(s)
    else:
        s = random_string(rng, "ab", N)
    return {"s": s}
