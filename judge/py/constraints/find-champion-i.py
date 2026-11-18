"""Find Champion I: an n x n tournament matrix (grid[i][j] == 1 means i beats j)."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    assert all(grid[i][i] == 0 for i in range(n)), "grid[i][i] is 0"
    assert all(grid[i][j] != grid[j][i] for i in range(n) for j in range(i + 1, n)), (
        "for i != j, grid[i][j] != grid[j][i]"
    )
    # A tournament is transitive exactly when its win counts are 0..n-1.
    assert sorted(sum(row) for row in grid) == list(range(n)), "stronger-than is transitive"
