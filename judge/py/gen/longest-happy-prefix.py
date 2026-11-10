"""Longest Happy Prefix at length 10^5: all one letter or a short repeated period (comparing
every prefix to its suffix is quadratic), or random letters."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 3
N = 10**5


def generate(rng):
    shape = rng.choice(["same", "period", "random"])
    if shape == "same":
        s = "a" * N
    elif shape == "period":
        unit = random_string(rng, "ab", rng.randint(2, 50))
        s = (unit * (N // len(unit) + 1))[: N - 1] + "z"
        if rng.random() < 0.5:
            s = (unit * (N // len(unit) + 1))[:N]
    else:
        s = random_string(rng, ascii_lowercase, N)
    return {"s": s}
