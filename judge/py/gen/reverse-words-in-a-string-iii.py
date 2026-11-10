"""Reverse Words III on 5 * 10^4 characters: printable non-space words joined by single spaces."""

from _shapes import random_string

SEEDS = 2
CHARS = [chr(c) for c in range(33, 127)]


def generate(rng):
    max_word = rng.choice([3, 20, 1000])
    words, total = [], 0
    while True:
        w = random_string(rng, CHARS, rng.randint(1, max_word))
        extra = len(w) + (1 if words else 0)
        if total + extra > 5 * 10**4:
            break
        words.append(w)
        total += extra
    return {"s": " ".join(words)}
