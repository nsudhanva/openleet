"""Partitioning Into Minimum Number Of Deci-Binary Numbers: a positive integer as a digit string."""


def check(n: str) -> None:
    assert isinstance(n, str), "n is a string"
    assert 1 <= len(n) <= 10**5, "1 <= n.length <= 10^5"
    assert all("0" <= c <= "9" for c in n), "n consists of only digits"
    assert n[0] != "0", "n does not contain any leading zeros and represents a positive integer"
