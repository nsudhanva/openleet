"""Minimum Operations to Make a Uni-Value Grid on a 100 x 100 grid with x = 1 or 2 and every value
congruent, so trying each of the thousands of distinct values as the target and summing over
the grid is quadratic in the cell count."""

SEEDS = 2
M = 100
N = 100
LIMIT = 10**4


def generate(rng):
    x = rng.randint(1, 2)
    r = rng.randint(1, x)
    grid = [[r + x * rng.randrange((LIMIT - r) // x + 1) for _ in range(N)] for _ in range(M)]
    return {"grid": grid, "x": x}
