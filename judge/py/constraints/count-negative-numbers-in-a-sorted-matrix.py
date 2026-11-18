"""Count Negative Numbers in a Sorted Matrix: a grid sorted non-increasingly in rows and columns."""


def check(grid: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 100, "1 <= m <= 100"
    n = len(grid[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert all(-100 <= v <= 100 for r in grid for v in r), "-100 <= grid[i][j] <= 100"
    assert all(r[j] >= r[j + 1] for r in grid for j in range(n - 1)), (
        "rows sorted in non-increasing order"
    )
    assert all(grid[i][j] >= grid[i + 1][j] for i in range(m - 1) for j in range(n)), (
        "columns sorted in non-increasing order"
    )
