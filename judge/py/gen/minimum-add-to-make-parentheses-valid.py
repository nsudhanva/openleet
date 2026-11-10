"""Minimum Add to Make Parentheses Valid at the maximum length 1000: random brackets or a
run of ')' then '('."""

from _shapes import random_string

SEEDS = 3


def generate(rng):
    if rng.random() < 0.5:
        return {"s": random_string(rng, "()", 1000)}
    cut = rng.randint(0, 1000)
    return {"s": ")" * cut + "(" * (1000 - cut)}
