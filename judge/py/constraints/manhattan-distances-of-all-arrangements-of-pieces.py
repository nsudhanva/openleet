"""Manhattan Distances of All Arrangements of Pieces: grid size m x n and piece count k."""


def check(m: int, n: int, k: int) -> None:
    assert 1 <= m <= 10**5 and 1 <= n <= 10**5, "1 <= m, n <= 10^5"
    assert 2 <= m * n <= 10**5, "2 <= m * n <= 10^5"
    assert 2 <= k <= m * n, "2 <= k <= m * n"
