"""Difference Between Ones and Zeros in Row and Column on a 4 x 25,000 or 25,000 x 4 grid, so
recounting a cell's row and column for every cell is ~2.5 * 10^9 steps."""

SEEDS = 2
LONG, SHORT = 25000, 4


def generate(rng):
    m, n = (SHORT, LONG) if rng.random() < 0.5 else (LONG, SHORT)
    density = rng.random()
    grid = [[int(rng.random() < density) for _ in range(n)] for _ in range(m)]
    return {"grid": grid}
