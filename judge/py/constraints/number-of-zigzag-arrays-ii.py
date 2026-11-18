"""Number of ZigZag Arrays II: length n and value range [l, r]."""


def check(n: int, l: int, r: int) -> None:  # noqa: E741
    assert 3 <= n <= 10**9, "3 <= n <= 10^9"
    assert 1 <= l < r <= 75, "1 <= l < r <= 75"
