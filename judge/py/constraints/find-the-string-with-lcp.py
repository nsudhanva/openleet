"""Find the String with LCP: an n x n matrix of lcp values."""


def check(lcp: list[list[int]]) -> None:
    n = len(lcp)
    assert 1 <= n <= 1000, "1 <= n == lcp.length <= 1000"
    assert all(len(row) == n for row in lcp), "n == lcp[i].length"
    assert all(0 <= v <= n for row in lcp for v in row), "0 <= lcp[i][j] <= n"
