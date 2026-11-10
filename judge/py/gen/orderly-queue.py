"""Orderly Queue at length 1000: k = 1 over a near-periodic string, the worst case for
comparing all rotations, or k > 1 where sorting is the answer."""

from _shapes import random_string

SEEDS = 3


def generate(rng):
    if rng.random() < 0.6:
        unit = random_string(rng, "ab", rng.randint(5, 20))
        s = (unit * 1000)[:1000]
        i = rng.randrange(1000)
        s = s[:i] + "a" + s[i + 1 :]
        return {"s": s, "k": 1}
    s = random_string(rng, "abcdefghijklmnopqrstuvwxyz", 1000)
    return {"s": s, "k": rng.randint(2, 1000)}
