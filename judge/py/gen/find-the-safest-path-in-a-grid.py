"""Safest Path on a 400 x 400 grid: a handful of thieves (distances up to hundreds), one thief in
a corner, or many scattered thieves."""

SEEDS = 3
N = 400


def generate(rng):
    grid = [[0] * N for _ in range(N)]
    shape = rng.randrange(3)
    if shape == 0:
        count = rng.randint(1, 8)
    elif shape == 1:
        grid[0][N - 1] = 1
        count = 0
    else:
        count = N * N // 50
    for _ in range(count):
        grid[rng.randrange(N)][rng.randrange(N)] = 1
    return {"grid": grid}
