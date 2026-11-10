"""Reorder List at the maximum 5 * 10^4 nodes (odd or even length)."""

SEEDS = 2


def generate(rng):
    n = rng.choice([5 * 10**4, 5 * 10**4 - 1])
    return {"head": [rng.randint(1, 1000) for _ in range(n)]}
