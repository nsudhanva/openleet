"""Bomb Enemy on a 400 x 400 grid of empty cells and enemies with almost no walls, so walking
the row and column out of every empty cell is ~10^8 steps."""

SEEDS = 2
N = 400


def generate(rng):
    p = rng.choice([0.3, 0.1])
    walls = rng.choice([0, 0.001])
    grid = []
    for _ in range(N):
        row = []
        for _ in range(N):
            r = rng.random()
            row.append("W" if r < walls else "E" if r < walls + p else "0")
        grid.append(row)
    return {"grid": grid}
