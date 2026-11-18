"""Maximize Points After Choosing K Tasks: two equal-length point lists and k."""


def check(technique1: list[int], technique2: list[int], k: int) -> None:
    n = len(technique1)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(technique2) == n, "n == technique1.length == technique2.length"
    assert all(1 <= v <= 10**5 for v in technique1), "1 <= technique1[i] <= 10^5"
    assert all(1 <= v <= 10**5 for v in technique2), "1 <= technique2[i] <= 10^5"
    assert 0 <= k <= n, "0 <= k <= n"
