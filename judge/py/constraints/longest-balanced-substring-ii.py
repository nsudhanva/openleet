"""Longest Balanced Substring II: a string over 'a', 'b', 'c'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "abc" for c in s), "s contains only the characters 'a', 'b', and 'c'"
