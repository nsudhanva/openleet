"""Word Subsets at 10^4 words on each side, where checking every pair is 10^8 comparisons;
words2 demands that only some of words1 meet."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 10**4


def generate(rng):
    narrow = rng.random() < 0.5
    alpha1 = "abcdef" if narrow else ascii_lowercase
    words1 = set()
    while len(words1) < N:
        words1.add(random_string(rng, alpha1, rng.randint(1, 10)))
    words1 = sorted(words1)
    rng.shuffle(words1)
    words2 = [random_string(rng, "abc", rng.randint(1, 2)) for _ in range(N)]
    return {"words1": words1, "words2": words2}
