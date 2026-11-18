"""Add Strings: two digit strings without leading zeros."""


def check(num1: str, num2: str) -> None:
    for s in (num1, num2):
        assert 1 <= len(s) <= 10**4, "1 <= num1.length, num2.length <= 10^4"
        assert s.isascii() and s.isdigit(), "num1 and num2 consist of only digits"
        assert s == "0" or s[0] != "0", "no leading zeros except for the zero itself"
