"""Detect Cycles in 2D Grid on 150 x 150: a comb of one letter (a spine plus every other row)
with lines of a second letter between its teeth, so no region has a cycle (or only a 2 x 2
block in the last corner does) and a fresh search from every cell is ~10^8 steps."""

from string import ascii_lowercase

SEEDS = 2
M = N = 150


def generate(rng):
    a, b, c = rng.sample(ascii_lowercase, 3)
    grid = [[a if i % 2 == 0 or j == 0 else b for j in range(N)] for i in range(M)]
    if rng.random() < 0.5:
        grid = [list(row) for row in zip(*grid, strict=True)]
    if rng.random() < 0.5:
        for i in (M - 2, M - 1):
            for j in (N - 2, N - 1):
                grid[i][j] = c
    return {"grid": grid}
