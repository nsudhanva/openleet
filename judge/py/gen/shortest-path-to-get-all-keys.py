"""Shortest Path to Get All Keys on a 30 x 30 grid with all 6 keys and locks scattered among
walls, so the (cell, keyset) BFS has 900 * 64 states."""

SEEDS = 3


def generate(rng):
    m, n = 30, 30
    k = rng.choice([6, 6, rng.randint(1, 5)])
    density = rng.choice([0.1, 0.25, 0.35])
    grid = [["#" if rng.random() < density else "." for _ in range(n)] for _ in range(m)]
    cells = rng.sample([(r, c) for r in range(m) for c in range(n)], 1 + 2 * k)
    r, c = cells[0]
    grid[r][c] = "@"
    for i in range(k):
        r, c = cells[1 + i]
        grid[r][c] = "abcdef"[i]
        r, c = cells[1 + k + i]
        grid[r][c] = "ABCDEF"[i]
    return {"grid": ["".join(row) for row in grid]}
