"""Number of ZigZag Arrays I: length n and value range [l, r]."""


def check(n: int, l: int, r: int) -> None:  # noqa: E741
    assert 3 <= n <= 2000, "3 <= n <= 2000"
    assert 1 <= l < r <= 2000, "1 <= l < r <= 2000"
