"""Kth Smallest Trimmed Number at the limits: 100 numbers of 100 digits and 100 queries, with
many equal trimmed values so ties must break by index."""

from _shapes import random_string

SEEDS = 2


def generate(rng):
    digits = rng.choice(["01", "0123456789"])
    nums = [random_string(rng, digits, 100) for _ in range(100)]
    queries = [[rng.randint(1, 100), rng.randint(1, 100)] for _ in range(100)]
    return {"nums": nums, "queries": queries}
