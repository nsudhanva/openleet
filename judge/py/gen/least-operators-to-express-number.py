"""Least Operators to Express Number with targets near 2 * 10^8, far beyond any search over
expressions."""

SEEDS = 3


def generate(rng):
    x = rng.choice([2, 3, rng.randint(2, 100), 100])
    return {"x": x, "target": rng.randint(10**8, 2 * 10**8)}
