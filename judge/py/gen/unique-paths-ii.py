"""Unique Paths II on grids up to 100 x 100 with obstacles, path counts kept within the
guaranteed 2 * 10^9 (thin 100 x 7 strips, or a full grid thickened until it fits)."""

SEEDS = 3
CAP = 2 * 10**9


def paths(grid):
    n = len(grid[0])
    row = [0] * n
    row[0] = 1
    for line in grid:
        for c in range(n):
            if line[c]:
                row[c] = 0
            elif c:
                row[c] += row[c - 1]
    return row[-1]


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        m, n = 100, 7  # C(105, 6) < 2 * 10^9 even with no obstacles
    elif shape == 1:
        m, n = 7, 100
    else:
        m, n = 100, 100
    p = 0.05 if shape < 2 else 0.25
    grid = [[1 if rng.random() < p else 0 for _ in range(n)] for _ in range(m)]
    grid[0][0] = grid[m - 1][n - 1] = 0
    while paths(grid) > CAP:
        for _ in range(100):
            r, c = rng.randrange(m), rng.randrange(n)
            if (r, c) not in ((0, 0), (m - 1, n - 1)):
                grid[r][c] = 1
    return {"obstacleGrid": grid}
