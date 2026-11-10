"""Number of Islands on a 300 x 300 grid: one random grid, and one checkerboard with 45,000
single-cell islands."""

SEEDS = 2
SIZE = 300


def generate(rng):
    if rng.random() < 0.5:
        grid = [["1" if (r + c) % 2 == 0 else "0" for c in range(SIZE)] for r in range(SIZE)]
    else:
        grid = [[rng.choice("01") for _ in range(SIZE)] for _ in range(SIZE)]
    return {"grid": grid}
