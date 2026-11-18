"""Minimum Cost Homecoming of a Robot in a Grid: start and home cells with row and column costs."""


def check(
    startPos: list[int], homePos: list[int], rowCosts: list[int], colCosts: list[int]
) -> None:
    m, n = len(rowCosts), len(colCosts)
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= c <= 10**4 for c in rowCosts), "0 <= rowCosts[r] <= 10^4"
    assert all(0 <= c <= 10**4 for c in colCosts), "0 <= colCosts[c] <= 10^4"
    assert len(startPos) == 2, "startPos.length == 2"
    assert len(homePos) == 2, "homePos.length == 2"
    assert 0 <= startPos[0] < m and 0 <= homePos[0] < m, "0 <= startrow, homerow < m"
    assert 0 <= startPos[1] < n and 0 <= homePos[1] < n, "0 <= startcol, homecol < n"
