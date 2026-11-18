"""Remove Palindromic Subsequences: a string of 'a' and 'b'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(c in "ab" for c in s), "s[i] is either 'a' or 'b'"
