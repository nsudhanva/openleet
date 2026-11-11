"""Number of Enclaves: two seeds are 120 by 120 grids with a random land band along the border, a
ring of water and dense land inside it, so flood-filling from every land cell to look for the
border costs the square of the ~5,000-cell enclave; one seed is a 500 by 500 serpentine land
path from a border cell with one gap, whose leftward rows need a pass each, so repeating
row-major relaxation sweeps until nothing changes is ~10^4 sweeps of 2.5 * 10^5 cells."""

from _shapes import pick_shape

SEEDS = 3
N = 120
BAND = 10
SNAKE = 500


def _band(rng):
    inner = rng.uniform(0.7, 0.8)
    grid = []
    for i in range(N):
        row = []
        for j in range(N):
            ring = min(i, j, N - 1 - i, N - 1 - j)
            if ring < BAND:
                row.append(int(rng.random() < 0.6))
            elif ring == BAND:
                row.append(0)
            else:
                row.append(int(rng.random() < inner))
        grid.append(row)
    return grid


def _snake(rng):
    n = SNAKE
    grid = [[0] * n for _ in range(n)]
    rows = range(1, n - 1, 2)
    for k, i in enumerate(rows):
        for j in range(1, n - 1):
            grid[i][j] = 1
        if k % 2 == 0:  # runs right, then steps down at the right end
            if i + 1 < n - 1:
                grid[i + 1][n - 2] = 1
        elif i + 1 < n - 1:
            grid[i + 1][1] = 1
    grid[1][0] = 1  # the one border cell the land escapes through
    # Cut the path in the middle third: the land after the cut is an enclave.
    cut = rng.randrange(len(rows) // 3, 2 * len(rows) // 3)
    grid[rows[cut]][rng.randint(n // 4, 3 * n // 4)] = 0
    return grid


def generate(rng):
    return {"grid": _snake(rng) if pick_shape(rng) == 1 else _band(rng)}
