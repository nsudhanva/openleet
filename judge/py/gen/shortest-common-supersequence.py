"""Shortest Common Supersequence on two 1000-letter strings over a small alphabet (O(n * m) DP
of 10^6 cells)."""

SEEDS = 2


def generate(rng):
    alphabet = rng.choice(["ab", "abcd", "abcdefghijklmnopqrstuvwxyz"])
    return {
        "str1": "".join(rng.choice(alphabet) for _ in range(1000)),
        "str2": "".join(rng.choice(alphabet) for _ in range(1000)),
    }
