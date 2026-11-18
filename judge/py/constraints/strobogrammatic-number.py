"""Strobogrammatic Number: a digit string without leading zeros."""


def check(num: str) -> None:
    assert isinstance(num, str), "num is a string"
    assert 1 <= len(num) <= 50, "1 <= num.length <= 50"
    assert all("0" <= c <= "9" for c in num), "num consists of only digits"
    assert num == "0" or num[0] != "0", "num has no leading zeros except for zero itself"
