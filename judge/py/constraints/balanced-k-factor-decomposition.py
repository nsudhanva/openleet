"""Balanced K-Factor Decomposition: n and the number of factors k."""


def check(n: int, k: int) -> None:
    assert 4 <= n <= 10**5, "4 <= n <= 10^5"
    assert 2 <= k <= 5, "2 <= k <= 5"
    divisors = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            divisors += 1 if d * d == n else 2
        d += 1
    assert k < divisors, "k is strictly less than the number of positive divisors of n"
