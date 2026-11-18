"""Decode Ways II: a string of digits and '*' wildcards."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "0123456789*" for c in s), "s[i] is a digit or '*'"
