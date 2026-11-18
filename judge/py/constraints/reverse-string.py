"""Reverse String: a list of printable ASCII characters."""


def check(s: list[str]) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(isinstance(c, str) and len(c) == 1 for c in s), "s[i] is a single character"
    assert all(32 <= ord(c) <= 126 for c in s), "s[i] is a printable ascii character"
