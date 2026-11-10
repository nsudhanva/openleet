"""Reverse Words on 10^4 characters of letters, digits and runs of spaces (leading, trailing and
multiple spaces between words)."""

from string import ascii_letters, digits

from _shapes import random_string

SEEDS = 2
WORD = ascii_letters + digits


def generate(rng):
    out = [" " * rng.randint(0, 5)]
    total = len(out[0])
    while True:
        word = random_string(rng, WORD, rng.randint(1, 8))
        gap = " " * rng.randint(1, 4)
        if total + len(word) + len(gap) > 10**4:
            break
        out.append(word)
        out.append(gap)
        total += len(word) + len(gap)
    return {"s": "".join(out)}
