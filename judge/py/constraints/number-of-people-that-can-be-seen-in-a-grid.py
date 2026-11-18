"""Number of People That Can Be Seen in a Grid: a grid of positive heights."""


def check(heights: list[list[int]]) -> None:
    assert 1 <= len(heights) <= 400, "1 <= heights.length <= 400"
    assert all(1 <= len(row) <= 400 for row in heights), "1 <= heights[i].length <= 400"
    assert all(1 <= v <= 10**5 for row in heights for v in row), "1 <= heights[i][j] <= 10^5"
