"""Count the Number of Special Characters II at length 2 * 10^5: random mixed case, or all
lowercase first then all uppercase (every letter special)."""

from _shapes import random_string

SEEDS = 2
N = 2 * 10**5
LOWER = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    if rng.random() < 0.5:
        word = random_string(rng, LOWER + LOWER.upper(), N)
    else:
        half = N // 2
        word = random_string(rng, LOWER, half)
        word += random_string(rng, LOWER.upper(), N - half)
    return {"word": word}
