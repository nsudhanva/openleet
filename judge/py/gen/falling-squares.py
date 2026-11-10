"""Falling Squares with 1000 squares over coordinates up to 10^8 (no dense array), heavily
overlapping so heights stack."""

SEEDS = 2
N = 1000


def generate(rng):
    span = rng.choice([10**4, 10**8 - 10**6])
    positions = [[rng.randint(1, span), rng.randint(1, 10**6)] for _ in range(N)]
    return {"positions": positions}
