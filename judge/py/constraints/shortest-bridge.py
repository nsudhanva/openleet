"""Shortest Bridge: an n x n binary grid with exactly two islands."""


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    assert all(v in (0, 1) for row in grid for v in row), "grid[i][j] is either 0 or 1"
    seen = [[False] * n for _ in range(n)]
    islands = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and not seen[i][j]:
                islands += 1
                seen[i][j] = True
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    for a, b in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and not seen[a][b]:
                            seen[a][b] = True
                            stack.append((a, b))
    assert islands == 2, "There are exactly two islands in grid"
