"""Score of a String on 100 random lowercase letters."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    return {"s": random_string(rng, "abcdefghijklmnopqrstuvwxyz", 100)}
