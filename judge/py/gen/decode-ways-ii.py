"""Decode Ways II at length 10^5: mostly '*', '1' and '2' so every position branches, or all
'*'."""

from _shapes import random_string

SEEDS = 2
N = 10**5


def generate(rng):
    s = "*" * N
    if rng.random() < 0.5:
        s = random_string(rng, "**12120123456789", N)
    return {"s": s}
