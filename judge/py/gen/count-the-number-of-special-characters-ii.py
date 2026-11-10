"""Count the Number of Special Characters II at length 2 * 10^5: random mixed case, or all
lowercase first then all uppercase (every letter special)."""

from string import ascii_letters, ascii_lowercase, ascii_uppercase

from _shapes import random_string

SEEDS = 2
N = 2 * 10**5


def generate(rng):
    if rng.random() < 0.5:
        word = random_string(rng, ascii_letters, N)
    else:
        half = N // 2
        word = random_string(rng, ascii_lowercase, half)
        word += random_string(rng, ascii_uppercase, N - half)
    return {"word": word}
