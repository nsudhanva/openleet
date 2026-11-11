"""Check if There is a Path With Equal Number of 0's And 1's on a 21 x 20 grid: alternating
diagonals give every path one 1 too few, but only at the last cell (and a few 1s turned 0 keep
it so), so exploring the paths without memoization is exponential."""

SEEDS = 2
M, N = 21, 20


def generate(rng):
    m, n = (M, N) if rng.random() < 0.5 else (N, M)
    grid = [[(i + j) % 2 for j in range(n)] for i in range(m)]
    grid[-1][-1] = 0
    for _ in range(m * n // 100):
        i, j = rng.randrange(m), rng.randrange(n)
        grid[i][j] = 0
    return {"grid": grid}
