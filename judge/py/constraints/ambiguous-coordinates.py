"""Ambiguous Coordinates: a string "(digits)"."""


def check(s: str) -> None:
    assert 4 <= len(s) <= 12, "4 <= s.length <= 12"
    assert s[0] == "(" and s[-1] == ")", "s[0] == '(' and s[s.length - 1] == ')'"
    assert all(c in "0123456789" for c in s[1:-1]), "The rest of s are digits"
