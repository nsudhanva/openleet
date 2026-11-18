"""Minimum Deletions to Make String Balanced: a string of 'a' and 'b'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "ab" for c in s), "s[i] is 'a' or 'b'"
