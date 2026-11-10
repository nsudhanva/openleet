"""Number of Strings That Appear as Substrings: 100 patterns and a 100-letter word over a tiny
alphabet, half the patterns real substrings and half near-misses."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alpha = "ab" if rng.random() < 0.5 else "abc"
    word = random_string(rng, alpha, 100)
    patterns = []
    for _ in range(100):
        if rng.random() < 0.5:
            i = rng.randrange(100)
            j = rng.randint(i + 1, 100)
            patterns.append(word[i:j])
        else:
            length = rng.randint(1, 100)
            patterns.append(random_string(rng, alpha, length))
    return {"patterns": patterns, "word": word}
