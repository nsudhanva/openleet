"""Swap Nodes in Pairs at the maximum 100 nodes, even or odd length."""

SEEDS = 2


def generate(rng):
    n = rng.choice([100, 99])
    return {"head": [rng.randint(0, 100) for _ in range(n)]}
