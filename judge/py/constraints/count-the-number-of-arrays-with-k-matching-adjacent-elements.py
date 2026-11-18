"""Count the Number of Arrays with K Matching Adjacent Elements: three integers n, m, k."""


def check(n: int, m: int, k: int) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= m <= 10**5, "1 <= m <= 10^5"
    assert 0 <= k <= n - 1, "0 <= k <= n - 1"
