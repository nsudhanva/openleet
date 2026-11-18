"""Palindrome Partitioning II: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 2000, "1 <= s.length <= 2000"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
