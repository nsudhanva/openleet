"""Minimum Number of Days to Eat N Oranges: a single integer n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 2 * 10**9, "1 <= n <= 2 * 10^9"
