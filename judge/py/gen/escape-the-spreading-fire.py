"""Escape the Spreading Fire on a 100 by 200 grid (transposed on one seed): an open L-shaped field
of ~7000 cells, and the fire at the far end of a ~6000-cell snake that opens beside the start, so
trying each waiting time in turn is ~6000 searches of the field."""

SEEDS = 2
M, N = 100, 200
BAND = 25


def generate(rng):
    grid = [[2] * N for _ in range(M)]
    # The field: the top BAND rows and the right BAND columns.
    for r in range(M):
        for c in range(N):
            if r < BAND or c >= N - BAND:
                grid[r][c] = 0
    # The snake fills the rest, behind a wall row and column, and opens on the field at (BAND, 0).
    width = N - BAND - 1
    rows = list(range(BAND + 1, M, 2))
    grid[BAND][0] = 0
    for k, r in enumerate(rows):
        grid[r][:width] = [0] * width
        if k:
            grid[r - 1][width - 1 if k % 2 else 0] = 0
    grid[rows[-1]][0 if len(rows) % 2 == 0 else width - 1] = 1
    if rng.random() < 0.5:
        # The start and the safehouse stay in their corners.
        grid = [list(col) for col in zip(*grid, strict=True)]
    return {"grid": grid}
