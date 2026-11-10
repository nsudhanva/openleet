"""Reverse Linked List at the maximum length (5000 nodes)."""

SEEDS = 2


def generate(rng):
    return {"head": [rng.randint(-5000, 5000) for _ in range(5000)]}
