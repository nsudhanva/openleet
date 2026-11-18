"""Permutation Sequence: n and the 1-based rank k."""

from math import factorial


def check(n: int, k: int) -> None:
    assert isinstance(n, int) and isinstance(k, int), "n and k are integers"
    assert 1 <= n <= 9, "1 <= n <= 9"
    assert 1 <= k <= factorial(n), "1 <= k <= n!"
