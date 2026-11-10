"""Flip String to Monotone Increasing at 10^5 characters: random, mostly-ones then mostly-zeros,
or alternating."""

from _shapes import random_string

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        s = random_string(rng, "01", N)
    elif shape == 1:
        h = N // 2
        s = "".join("1" if rng.random() < 0.9 else "0" for _ in range(h))
        s += "".join("0" if rng.random() < 0.9 else "1" for _ in range(N - h))
    else:
        s = "01" * (N // 2)
    return {"s": s}
