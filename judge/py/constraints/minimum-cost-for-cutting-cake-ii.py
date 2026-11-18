"""Minimum Cost for Cutting Cake II: cake size m x n with horizontal and vertical cut costs."""


def check(m: int, n: int, horizontalCut: list[int], verticalCut: list[int]) -> None:
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(horizontalCut) == m - 1, "horizontalCut.length == m - 1"
    assert len(verticalCut) == n - 1, "verticalCut.length == n - 1"
    assert all(1 <= v <= 10**3 for v in horizontalCut), "1 <= horizontalCut[i] <= 10^3"
    assert all(1 <= v <= 10**3 for v in verticalCut), "1 <= verticalCut[i] <= 10^3"
