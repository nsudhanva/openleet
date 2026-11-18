"""Smallest Integer Divisible by K: a positive integer k."""


def check(k: int) -> None:
    assert isinstance(k, int), "k is an integer"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
