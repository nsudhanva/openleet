"""Longest Word in Dictionary with 1000 words: several buildable prefix chains up to length 30
competing on length and lexicographic order, plus words with a missing prefix."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    words = set()
    while len(words) < 1000:
        base = random_string(rng, "abc", rng.randint(5, 30))
        stop = len(base) if rng.random() < 0.6 else rng.randint(1, len(base))
        for i in range(1, len(base) + 1):
            if i == stop + 1 and stop < len(base):
                continue
            words.add(base[:i])
            if len(words) >= 1000:
                break
    words = sorted(words)
    rng.shuffle(words)
    return {"words": words}
