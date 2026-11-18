"""Digit Operations to Make Two Integers Equal: two integers with the same digit count."""


def check(n: int, m: int) -> None:
    assert 1 <= n < 10**4 and 1 <= m < 10**4, "1 <= n, m < 10^4"
    assert len(str(n)) == len(str(m)), "n and m consist of the same number of digits"
