"""Minimum Cost to Separate Sentence Into Rows on a 5000-character sentence of 1-3 letter words
with k = 6 to 10, so recursing over the row breaks without memoizing is exponential."""

from _shapes import random_string

SEEDS = 2
LENGTH = 5000
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    words, size = [], -1
    while True:
        word = random_string(rng, LETTERS, rng.randint(1, 3))
        if size + 1 + len(word) > LENGTH:
            break
        words.append(word)
        size += 1 + len(word)
    return {"sentence": " ".join(words), "k": rng.randint(6, 10)}
