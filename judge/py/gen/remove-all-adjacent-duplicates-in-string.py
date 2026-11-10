"""Remove Adjacent Duplicates at length 10^5: a nested palindrome that collapses completely
from the middle out, or random two-letter text with long cascades."""

from _shapes import random_string

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        half = random_string(rng, "ab", N // 2)
        s = half + half[::-1]
    else:
        s = random_string(rng, "ab", N)
    return {"s": s}
