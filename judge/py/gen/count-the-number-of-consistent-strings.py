"""Count the Number of Consistent Strings with 10^4 words of length 10 and a mid-sized
allowed set, so about half the words need a full scan."""

from _shapes import random_string

SEEDS = 2
W = 10**4
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    allowed = "".join(rng.sample(LETTERS, rng.randint(1, 26)))
    words = []
    for _ in range(W):
        if rng.random() < 0.5:
            words.append(random_string(rng, allowed, 10))
        else:
            words.append(random_string(rng, LETTERS, rng.randint(1, 10)))
    return {"allowed": allowed, "words": words}
