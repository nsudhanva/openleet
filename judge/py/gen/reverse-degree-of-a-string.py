"""Reverse Degree on a 1000-letter random lowercase string."""

SEEDS = 2


def generate(rng):
    return {"s": "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(1000))}
