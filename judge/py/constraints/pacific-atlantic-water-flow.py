"""Pacific Atlantic Water Flow: an m x n grid of heights."""


def check(heights: list[list[int]]) -> None:
    m = len(heights)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(heights[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in heights), "n == heights[r].length"
    assert all(0 <= h <= 10**5 for row in heights for h in row), "0 <= heights[r][c] <= 10^5"
