"""Twisted Mirror Path Count on a 60 x 60 grid with 20% mirrors, so enumerating paths one by one
(~10^30 of them) never finishes while the grid DP is 3600 cells."""

SEEDS = 2
M = N = 60


def generate(rng):
    grid = [[1 if rng.random() < 0.2 else 0 for _ in range(N)] for _ in range(M)]
    grid[0][0] = grid[-1][-1] = 0
    return {"grid": grid}
