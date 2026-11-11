"""Minimum Time to Visit a Cell at 316 x 316 (~10^5 cells): a serpentine corridor of low cells
(along rows, or columns) between walls of 5 * 10^4 to 10^5, so the best path is ~5 * 10^4 steps
long and relaxing every cell until nothing changes takes tens of thousands of sweeps."""

SEEDS = 2
M = 316
WALL = 10**5


def generate(rng):
    transpose = rng.randrange(2)  # seed 0 runs along columns, seed 1 along rows
    grid = [[rng.randint(WALL // 2, WALL) for _ in range(M)] for _ in range(M)]
    step = 0
    for r in range(0, M, 2):
        cols = range(M) if r % 4 == 0 else range(M - 1, -1, -1)
        for c in cols:
            grid[r][c] = rng.randint(0, step) if step else 0
            step += 1
        if r + 1 < M:
            c = M - 1 if r % 4 == 0 else 0
            grid[r + 1][c] = rng.randint(0, step)
            step += 1
    if M % 2 == 0:
        grid[M - 1][M - 1] = rng.randint(0, step)
    if transpose:
        grid = [list(col) for col in zip(*grid, strict=True)]
    grid[0][0] = 0
    return {"grid": grid}
