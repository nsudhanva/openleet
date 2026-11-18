"""Bricks Falling When Hit: a binary grid and a list of distinct cells to erase."""


def check(grid: list[list[int]], hits: list[list[int]]) -> None:
    m = len(grid)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(grid[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    assert all(v in (0, 1) for r in grid for v in r), "grid[i][j] is 0 or 1"
    assert 1 <= len(hits) <= 4 * 10**4, "1 <= hits.length <= 4 * 10^4"
    assert all(len(h) == 2 for h in hits), "hits[i].length == 2"
    assert all(0 <= x <= m - 1 for x, _ in hits), "0 <= xi <= m - 1"
    assert all(0 <= y <= n - 1 for _, y in hits), "0 <= yi <= n - 1"
    assert len({(x, y) for x, y in hits}) == len(hits), "All (xi, yi) are unique"
