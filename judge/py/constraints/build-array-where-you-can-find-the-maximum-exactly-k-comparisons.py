"""Build Array Where You Can Find The Maximum Exactly K Comparisons: n, m, k."""


def check(n: int, m: int, k: int) -> None:
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert 1 <= m <= 100, "1 <= m <= 100"
    assert 0 <= k <= n, "0 <= k <= n"
