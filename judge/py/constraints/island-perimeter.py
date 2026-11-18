"""Island Perimeter: a 0/1 grid holding exactly one island."""


def check(grid: list[list[int]]) -> None:
    assert isinstance(grid, list) and all(isinstance(r, list) for r in grid), "grid is a 2D list"
    rows = len(grid)
    assert 1 <= rows <= 100, "1 <= row <= 100"
    cols = len(grid[0])
    assert 1 <= cols <= 100, "1 <= col <= 100"
    assert all(len(r) == cols for r in grid), "col == grid[i].length"
    assert all(v in (0, 1) for r in grid for v in r), "grid[i][j] is 0 or 1"
    seen = [[False] * cols for _ in range(rows)]
    islands = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and not seen[i][j]:
                islands += 1
                seen[i][j] = True
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if (
                            0 <= nx < rows
                            and 0 <= ny < cols
                            and grid[nx][ny] == 1
                            and not seen[nx][ny]
                        ):
                            seen[nx][ny] = True
                            stack.append((nx, ny))
    assert islands == 1, "there is exactly one island in grid"
