"""New 21 Game: the integers n, k and maxPts."""


def check(n: int, k: int, maxPts: int) -> None:
    assert 0 <= k <= n <= 10**4, "0 <= k <= n <= 10^4"
    assert 1 <= maxPts <= 10**4, "1 <= maxPts <= 10^4"
