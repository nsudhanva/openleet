"""Flip String to Monotone Increasing: a binary string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "01" for c in s), "s[i] is either '0' or '1'"
