"""Shortest Palindrome: a lowercase string, possibly empty."""


def check(s: str) -> None:
    assert 0 <= len(s) <= 5 * 10**4, "0 <= s.length <= 5 * 10^4"
    assert all("a" <= ch <= "z" for ch in s), "s consists of lowercase English letters only"
