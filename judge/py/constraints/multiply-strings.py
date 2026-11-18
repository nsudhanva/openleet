"""Multiply Strings: two non-negative integers as digit strings."""


def check(num1: str, num2: str) -> None:
    for s in (num1, num2):
        assert 1 <= len(s) <= 200, "1 <= num1.length, num2.length <= 200"
        assert s.isascii() and s.isdigit(), "num1 and num2 consist of digits only"
        assert s == "0" or s[0] != "0", "no leading zero, except the number 0 itself"
