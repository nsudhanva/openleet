"""Longest Palindrome (letter counts) on 2000 mixed-case letters."""

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate(rng):
    alphabet = rng.choice([LETTERS, "aA"])
    return {"s": "".join(rng.choice(alphabet) for _ in range(2000))}
