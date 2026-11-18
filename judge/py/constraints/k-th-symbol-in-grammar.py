"""K-th Symbol in Grammar: row number n and position k."""


def check(n: int, k: int) -> None:
    assert 1 <= n <= 30, "1 <= n <= 30"
    assert 1 <= k <= 2**n - 1, "1 <= k <= 2^n - 1"
