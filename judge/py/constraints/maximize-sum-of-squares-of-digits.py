"""Maximize Sum of Squares of Digits: a digit count num and a digit sum."""


def check(num: int, sum: int) -> None:
    assert 1 <= num <= 2 * 10**5, "1 <= num <= 2 * 10^5"
    assert 1 <= sum <= 2 * 10**6, "1 <= sum <= 2 * 10^6"
