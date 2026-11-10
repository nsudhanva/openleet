"""Repeated DNA Sequences at length 10^5: random ACGT, or a short-period sequence where nearly
every 10-letter window repeats."""

from _shapes import random_string

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        s = random_string(rng, "ACGT", N)
    else:
        unit = random_string(rng, "ACGT", rng.randint(11, 400))
        s = list((unit * (N // len(unit) + 1))[:N])
        for _ in range(200):
            s[rng.randrange(N)] = rng.choice("ACGT")
        s = "".join(s)
    return {"s": s}
