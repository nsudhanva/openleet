"""To Lower Case at the maximum 100 printable ASCII characters, mixing letters with the
symbols just outside 'A'..'Z' ('@', '[')."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    chars = [chr(c) for c in range(32, 127)] + list("@[AZaz") * 5
    return {"s": random_string(rng, chars, 100)}
