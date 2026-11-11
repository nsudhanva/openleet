"""Number of Corner Rectangles on sixteen 200 x 200 grids where every row holds two to four ones,
drawn from 60 columns so rectangles exist: every one of the 19900 row pairs shares columns to
compare, ~8 * 10^6 cell tests per seed for a pair-of-rows scan against ~10^3 for the intended
counting, and the sixteen seeds add up."""

SEEDS = 16
M = 200
POOL = 60


def generate(rng):
    columns = rng.sample(range(M), POOL)
    grid = [[0] * M for _ in range(M)]
    for row in grid:
        for c in rng.sample(columns, rng.randint(2, 4)):
            row[c] = 1
    return {"grid": grid}
