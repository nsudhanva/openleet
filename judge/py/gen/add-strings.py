"""Add Strings at length 10^4: all-nines plus one carries through every digit; random digits
otherwise."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    if rng.random() < 0.5:
        return {"num1": "9" * 10**4, "num2": "1"}
    a = str(rng.randint(1, 9)) + random_string(rng, "0123456789", 10**4 - 1)
    b = str(rng.randint(1, 9)) + random_string(rng, "0123456789", rng.randint(0, 10**4 - 1))
    return {"num1": a, "num2": b}
