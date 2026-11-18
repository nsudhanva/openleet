"""Cracking the Safe: password length n and digit count k."""


def check(n: int, k: int) -> None:
    assert 1 <= n <= 4, "1 <= n <= 4"
    assert 1 <= k <= 10, "1 <= k <= 10"
    assert 1 <= k**n <= 4096, "1 <= k^n <= 4096"
