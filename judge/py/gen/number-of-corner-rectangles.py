"""Number of Corner Rectangles at 200 x 200 with the 6000 ones in 60 rows of 100, so checking
every pair of rows against every pair of columns is ~4 * 10^8 steps."""

SEEDS = 2
M = 200
ROWS = 60
ONES = 6000


def generate(rng):
    grid = [[0] * M for _ in range(M)]
    for r in rng.sample(range(M), ROWS):
        for c in rng.sample(range(M), ONES // ROWS):
            grid[r][c] = 1
    return {"grid": grid}
