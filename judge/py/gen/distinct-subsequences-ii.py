"""Distinct Subsequences II at length 2000: random letters, or a tiny alphabet with many
repeats so duplicate subsequences must be subtracted."""

SEEDS = 2
L = 2000


def generate(rng):
    alphabet = "abcdefghijklmnopqrstuvwxyz" if rng.random() < 0.5 else "ab"
    return {"s": "".join(rng.choice(alphabet) for _ in range(L))}
