"""Palindromic Substrings at length 1000: all one letter (every substring is a palindrome),
or random over two letters."""

SEEDS = 2
N = 1000


def generate(rng):
    s = "a" * N if rng.random() < 0.5 else "".join(rng.choice("ab") for _ in range(N))
    return {"s": s}
