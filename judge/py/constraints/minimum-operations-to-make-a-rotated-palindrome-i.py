"""Minimum Operations to Make a Rotated Palindrome I: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 2 <= len(s) <= 2000, "2 <= s.length <= 2000"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
