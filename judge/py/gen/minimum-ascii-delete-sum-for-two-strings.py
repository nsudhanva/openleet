"""Minimum ASCII Delete Sum at 1000 x 1000 characters: a small alphabet so the strings share
long subsequences, or the full alphabet."""

SEEDS = 3


def generate(rng):
    alphabet = rng.choice(("ab", "abcd", "abcdefghijklmnopqrstuvwxyz"))
    return {
        "s1": "".join(rng.choice(alphabet) for _ in range(1000)),
        "s2": "".join(rng.choice(alphabet) for _ in range(1000)),
    }
