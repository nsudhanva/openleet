"""Minimum Cost Path With Teleportations on an 80 x 80 grid with k = 10, the start 0 and the goal
the largest value so no single teleport finishes, so scanning every cell for each cell's best
teleport source is 10 * 6400^2 steps."""

SEEDS = 2
SIDE = 80
K = 10
LIMIT = 10**4


def generate(rng):
    grid = [[rng.randint(0, LIMIT) for _ in range(SIDE)] for _ in range(SIDE)]
    grid[0][0] = 0
    grid[-1][-1] = LIMIT
    return {"grid": grid, "k": K}
