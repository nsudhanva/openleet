"""Short Encoding with 2000 words of length <= 7 over a tiny alphabet, so many words are
suffixes of others (and some repeat)."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alphabet = rng.choice(["ab", "abc", ascii_lowercase])
    words = []
    for _ in range(2000):
        words.append(random_string(rng, alphabet, rng.randint(1, 7)))
    return {"words": words}
