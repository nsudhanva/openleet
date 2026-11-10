"""Maximum Product of Word Lengths with 1000 words of up to 1000 letters each, drawn from
small random alphabets so only some pairs share no letter; pairwise set comparison is slow."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    words = []
    for _ in range(1000):
        alphabet = rng.sample(ascii_lowercase, rng.randint(1, 13))
        length = rng.randint(1, 1000)
        words.append(random_string(rng, alphabet, length))
    return {"words": words}
