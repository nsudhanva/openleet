"""Map of Highest Peak at 300 x 300 with 3000 to 5000 water cells at random, or a 1000 x 480 grid
with water only along the bottom or the top row (heights up to 999), so measuring every cell
against every water cell, a separate search from each water cell, or relaxing cells in sweeps
until nothing changes is >= 10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
M = 300
WATER = (3000, 5000)
TALL, WIDE = 1000, 480


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        grid = [[0] * M for _ in range(M)]
        for cell in rng.sample(range(M * M), rng.randint(*WATER)):
            grid[cell // M][cell % M] = 1
        return {"isWater": grid}
    grid = [[0] * WIDE for _ in range(TALL)]
    grid[TALL - 1 if shape == 1 else 0] = [1] * WIDE
    return {"isWater": grid}
