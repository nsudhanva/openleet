"""Largest Odd Number in String: a digit string without leading zeros."""


def check(num: str) -> None:
    assert isinstance(num, str), "num is a string"
    assert 1 <= len(num) <= 10**5, "1 <= num.length <= 10^5"
    assert all(c in "0123456789" for c in num), "num only consists of digits"
    assert num == "0" or num[0] != "0", "num does not contain any leading zeros"
