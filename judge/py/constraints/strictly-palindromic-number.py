"""Strictly Palindromic Number: an integer n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 4 <= n <= 10**5, "4 <= n <= 10^5"
