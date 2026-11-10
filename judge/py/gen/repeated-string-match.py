"""Repeated String Match with |a|, |b| up to 10^4 over a near-periodic alphabet: b is a slice
of a repeated many times (answer exists), or the same slice with one letter changed (-1)."""

from _shapes import random_string

SEEDS = 3


def generate(rng):
    unit = random_string(rng, "ab", rng.randint(1, 4))
    la = rng.randint(50, 500)
    a = (unit * la)[:la]
    a = a[:-1] + ("b" if a[-1] == "a" else "a")
    start = rng.randrange(la)
    lb = rng.randint(9000, 10**4)
    b = list((a * (lb // la + 3))[start : start + lb])
    if rng.random() < 0.4:
        i = rng.randrange(lb)
        b[i] = "c"
    return {"a": a, "b": "".join(b)}
