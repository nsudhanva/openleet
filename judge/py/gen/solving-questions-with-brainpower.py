"""Solving Questions With Brainpower at n = 10^5: small brainpower (dense choices) or huge
brainpower; point totals exceed 32 bits."""

SEEDS = 3
N = 10**5


def generate(rng):
    hi = rng.choice([3, 100, 10**5])
    return {"questions": [[rng.randint(1, 10**5), rng.randint(1, hi)] for _ in range(N)]}
