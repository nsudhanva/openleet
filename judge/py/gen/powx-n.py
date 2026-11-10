"""Pow(x, n) with |n| near 2^31 and x within a few billionths of +-1, so x^n stays inside
[-10^4, 10^4] while a linear multiply loop takes billions of steps."""

import math

SEEDS = 3


def generate(rng):
    while True:
        n = rng.choice([2**31 - 1, -(2**31), rng.randint(2**30, 2**31 - 1)])
        d = rng.randint(1, 40) / 10**10
        x = 1.0 + d if rng.random() < 0.5 else 1.0 - d
        if rng.random() < 0.3:
            x = -x
        x = round(x, 12)
        logmag = n * math.log(abs(x))
        if -30 < logmag < math.log(10**4) - 0.5:
            return {"x": x, "n": n}
