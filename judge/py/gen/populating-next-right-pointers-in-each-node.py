"""Populating Next Right Pointers on the largest perfect binary tree, 2^12 - 1 = 4095 nodes."""

SEEDS = 2


def generate(rng):
    return {"root": [rng.randint(-1000, 1000) for _ in range(2**12 - 1)]}
