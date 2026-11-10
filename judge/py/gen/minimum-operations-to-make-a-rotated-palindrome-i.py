"""Minimum Operations to Make a Rotated Palindrome I at the maximum length 2000: random
letters or a near-palindrome, rotated."""

from _shapes import random_string

SEEDS = 3
N = 2000
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    if rng.random() < 0.5:
        return {"s": random_string(rng, LETTERS, N)}
    half = [rng.choice(LETTERS) for _ in range(N // 2)]
    chars = half + half[::-1]
    for _ in range(rng.randint(1, 20)):
        chars[rng.randrange(N)] = rng.choice(LETTERS)
    cut = rng.randrange(N)
    return {"s": "".join(chars[cut:] + chars[:cut])}
