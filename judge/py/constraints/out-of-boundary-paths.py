"""Out of Boundary Paths: grid size m x n, a move budget and a start cell."""


def check(m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> None:
    assert 1 <= m <= 50 and 1 <= n <= 50, "1 <= m, n <= 50"
    assert 0 <= maxMove <= 50, "0 <= maxMove <= 50"
    assert 0 <= startRow < m, "0 <= startRow < m"
    assert 0 <= startColumn < n, "0 <= startColumn < n"
