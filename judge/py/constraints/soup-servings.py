"""Soup Servings: the starting volume n of each soup."""


def check(n: int) -> None:
    assert isinstance(n, int) and 0 <= n <= 10**9, "0 <= n <= 10^9"
