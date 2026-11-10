"""Count the Number of Special Characters II at length 2 * 10^5: random mixed case, or all
lowercase first then all uppercase (every letter special)."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 2 * 10**5


def generate(rng):
    if rng.random() < 0.5:
        word = random_string(rng, ascii_lowercase + ascii_lowercase.upper(), N)
    else:
        half = N // 2
        word = random_string(rng, ascii_lowercase, half)
        word += random_string(rng, ascii_lowercase.upper(), N - half)
    return {"word": word}
