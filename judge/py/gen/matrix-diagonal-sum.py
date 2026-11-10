"""Matrix Diagonal Sum on 100 x 100 or 99 x 99 matrices (odd size shares the center)."""

SEEDS = 2


def generate(rng):
    n = rng.choice([100, 99])
    return {"mat": [[rng.randint(1, 100) for _ in range(n)] for _ in range(n)]}
