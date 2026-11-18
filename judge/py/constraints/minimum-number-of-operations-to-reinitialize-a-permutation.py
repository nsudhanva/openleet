"""Minimum Number of Operations to Reinitialize a Permutation: an even integer n."""


def check(n: int) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert n % 2 == 0, "n is even"
