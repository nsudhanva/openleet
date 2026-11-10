"""Longest String Chain with 1000 words: a planted chain of length 16 plus many words that
share its letters, or random words of every length."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    words = set()
    if rng.random() < 0.5:
        for _ in range(rng.randint(3, 8)):
            word = ""
            for _ in range(16):
                i = rng.randint(0, len(word))
                word = word[:i] + rng.choice("abc") + word[i:]
                words.add(word)
    while len(words) < 1000:
        n = rng.randint(1, 16)
        words.add(random_string(rng, "abc" if n < 8 else ascii_lowercase, n))
    words = sorted(words)
    rng.shuffle(words)
    return {"words": words}
