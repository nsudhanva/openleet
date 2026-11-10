"""Minimum Insertions to Balance a Parentheses String at length 10^5: random brackets, or
'(' runs followed by odd-length ')' runs."""

from _shapes import random_string

SEEDS = 3
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        return {"s": random_string(rng, "()", N)}
    parts, size = [], 0
    while size < N:
        run = "(" * rng.randint(1, 50) + ")" * rng.randint(1, 101)
        parts.append(run)
        size += len(run)
    return {"s": "".join(parts)[:N]}
