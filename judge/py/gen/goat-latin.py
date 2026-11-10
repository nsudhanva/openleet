"""Goat Latin at up to 150 characters: many short words (the 'a' suffix grows fastest) mixing
upper- and lowercase vowels and consonants."""

from _shapes import random_string

SEEDS = 2
LETTERS = "aeiouAEIOUbcdfgBCDFGxyzXYZ"


def generate(rng):
    words, length = [], 0
    while True:
        w = random_string(rng, LETTERS, rng.randint(1, 3))
        extra = len(w) + (1 if words else 0)
        if length + extra > 150:
            break
        words.append(w)
        length += extra
    return {"sentence": " ".join(words)}
