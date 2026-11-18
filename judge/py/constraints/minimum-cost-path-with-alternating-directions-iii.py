"""Minimum Cost Path with Alternating Directions III: grid size m x n and a penalty grid."""


def check(m: int, n: int, penalty: list[list[int]]) -> None:
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 2 <= m * n <= 10**5, "2 <= m * n <= 10^5"
    assert len(penalty) == m, "penalty.length == m"
    assert all(len(row) == n for row in penalty), "penalty[i].length == n"
    assert all(0 <= v <= 10**5 for row in penalty for v in row), "0 <= penalty[i][j] <= 10^5"
