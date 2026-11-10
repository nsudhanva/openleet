"""Longest Palindromic Subsequence at length 1000 (exponential without DP), over a tiny or
full alphabet."""

SEEDS = 2


def generate(rng):
    alphabet = rng.choice(["ab", "abcdefghijklmnopqrstuvwxyz"])
    return {"s": "".join(rng.choice(alphabet) for _ in range(1000))}
