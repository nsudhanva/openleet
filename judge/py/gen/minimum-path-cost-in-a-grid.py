"""Minimum Path Cost in a Grid on a 12 x 12 grid, so trying every path by plain recursion (12^12 of
them) never finishes while the row-by-row DP is ~1700 steps."""

SEEDS = 2
M = 12
N = 12


def generate(rng):
    values = rng.sample(range(M * N), M * N)
    grid = [values[i * N : (i + 1) * N] for i in range(M)]
    move_cost = [[rng.randint(1, 100) for _ in range(N)] for _ in range(M * N)]
    return {"grid": grid, "moveCost": move_cost}
