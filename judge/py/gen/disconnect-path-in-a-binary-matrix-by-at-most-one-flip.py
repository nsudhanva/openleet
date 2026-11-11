"""Disconnect Path in a Binary Matrix by at Most One Flip on a ~10^5-cell grid: the top and right
border and the left and bottom border are the only two (disjoint) paths, and the interior is a big
dead end both can enter, so blocking each path cell and searching again is ~6 * 10^7 steps."""

SEEDS = 2
CELLS = 10**5


def generate(rng):
    m = rng.randint(200, 500)
    n = CELLS // m
    grid = [[int(rng.random() < 0.9) for _ in range(n)] for _ in range(m)]
    for j in range(n):
        grid[0][j] = grid[m - 1][j] = 1
        if 0 < j < n - 1:
            grid[m - 2][j] = 0  # nothing in the interior steps down onto the bottom row
    for i in range(m):
        grid[i][0] = grid[i][n - 1] = 1
        if 0 < i < m - 1:
            grid[i][n - 2] = 0  # or right onto the right column
    return {"grid": grid}
