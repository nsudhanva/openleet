"""Odd Even Linked List at the maximum length 10^4."""

SEEDS = 2


def generate(rng):
    n = rng.choice([10**4, 10**4 - 1])
    return {"head": [rng.randint(-(10**6), 10**6) for _ in range(n)]}
