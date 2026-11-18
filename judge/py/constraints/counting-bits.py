"""Counting Bits: a single integer n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 0 <= n <= 10**5, "0 <= n <= 10^5"
