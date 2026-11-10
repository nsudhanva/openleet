"""Longest Common Subsequence with both strings at length 1000, over a tiny alphabet (long
answer) or the full alphabet."""

SEEDS = 2
N = 1000


def generate(rng):
    alphabet = rng.choice(["ab", "abcd", "abcdefghijklmnopqrstuvwxyz"])
    return {
        "text1": "".join(rng.choice(alphabet) for _ in range(N)),
        "text2": "".join(rng.choice(alphabet) for _ in range(N)),
    }
