"""Number of Sets of K Non-Overlapping Line Segments: points n and segments k."""


def check(n: int, k: int) -> None:
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert 1 <= k <= n - 1, "1 <= k <= n-1"
