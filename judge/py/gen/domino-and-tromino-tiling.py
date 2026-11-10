"""Domino and Tromino Tiling at n near 1000, where unmemoized recursion is exponential."""

SEEDS = 2


def generate(rng):
    return {"n": rng.choice([1000, rng.randint(900, 999)])}
