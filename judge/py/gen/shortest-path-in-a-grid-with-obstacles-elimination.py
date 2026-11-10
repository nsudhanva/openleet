"""Shortest Path with Obstacles Elimination on a 40 x 40 grid with dense obstacles and a mid-sized
k, so the (cell, k) state space is large."""

SEEDS = 3


def generate(rng):
    m, n = 40, 40
    density = rng.choice([0.3, 0.5, 0.7])
    grid = [[1 if rng.random() < density else 0 for _ in range(n)] for _ in range(m)]
    grid[0][0] = 0
    grid[m - 1][n - 1] = 0
    k = rng.choice([rng.randint(1, 10), rng.randint(10, 40), rng.randint(1, m * n)])
    return {"grid": grid, "k": k}
