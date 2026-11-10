"""Simplify Path at ~3000 characters: names, '.', '..', '...', and runs of slashes, with deep
nesting and many pops."""

from _shapes import random_string

SEEDS = 3
NAME = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_."


def generate(rng):
    out = "/"
    pop_rate = rng.choice([0.1, 0.4, 0.6])
    while True:
        r = rng.random()
        if r < pop_rate:
            part = ".."
        elif r < pop_rate + 0.1:
            part = "."
        elif r < pop_rate + 0.15:
            part = "..."
        else:
            part = random_string(rng, NAME, rng.randint(1, 6))
        piece = part + "/" * rng.randint(1, 3)
        if len(out) + len(piece) > 3000:
            break
        out += piece
    return {"path": out}
