"""Minimum Addition to Make Integer Beautiful: a positive integer n and a digit-sum target."""


def check(n: int, target: int) -> None:
    assert 1 <= n <= 10**12, "1 <= n <= 10^12"
    assert 1 <= target <= 150, "1 <= target <= 150"
