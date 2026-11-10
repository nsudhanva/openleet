"""Reverse String II on 10^4 lowercase letters with k small (many chunks), mid, or >= n."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 3


def generate(rng):
    s = random_string(rng, ascii_lowercase, 10**4)
    k = rng.choice([1, rng.randint(2, 50), rng.randint(51, 9999), 10**4])
    return {"s": s, "k": k}
