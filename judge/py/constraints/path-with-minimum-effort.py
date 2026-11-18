"""Path With Minimum Effort: a grid of heights."""


def check(heights: list[list[int]]) -> None:
    assert isinstance(heights, list) and heights, "heights is a non-empty matrix"
    rows = len(heights)
    assert 1 <= rows <= 100, "1 <= rows <= 100"
    cols = len(heights[0]) if isinstance(heights[0], list) else 0
    assert all(isinstance(r, list) and len(r) == cols for r in heights), (
        "columns == heights[i].length"
    )
    assert 1 <= cols <= 100, "1 <= columns <= 100"
    assert all(isinstance(v, int) and 1 <= v <= 10**6 for r in heights for v in r), (
        "1 <= heights[i][j] <= 10^6"
    )
