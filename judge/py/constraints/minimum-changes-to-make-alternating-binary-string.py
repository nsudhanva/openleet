"""Minimum Changes To Make Alternating Binary String: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all(c in "01" for c in s), "s[i] is either '0' or '1'"
