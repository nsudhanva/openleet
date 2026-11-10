"""Count Different Palindromic Subsequences at length 1000 over 'abcd': random, or a
repeated palindrome-heavy pattern."""

from _shapes import random_string

SEEDS = 2
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        s = random_string(rng, "abcd", N)
    else:
        half = random_string(rng, "abcd", N // 2)
        s = half + half[::-1]
    return {"s": s}
