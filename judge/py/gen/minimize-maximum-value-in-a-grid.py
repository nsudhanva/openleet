"""Minimize Maximum Value in a Grid on a 1000 x 100 grid of distinct values, the shape with the
longest rows plus columns, so scanning the row and column of every cell is cubic."""

SEEDS = 2
ROWS = 1000
COLS = 100
LIMIT = 10**9


def generate(rng):
    vals = rng.sample(range(1, LIMIT + 1), ROWS * COLS)
    return {"grid": [vals[i * COLS : (i + 1) * COLS] for i in range(ROWS)]}
