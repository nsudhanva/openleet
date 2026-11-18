"""Minimum Number of Moves to Make Palindrome: a lowercase string that can become a
palindrome."""

from collections import Counter


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 2000, "1 <= s.length <= 2000"
    assert all("a" <= c <= "z" and len(c) == 1 for c in s), (
        "s consists only of lowercase English letters"
    )
    odd = sum(c % 2 for c in Counter(s).values())
    assert odd <= 1, "s can be converted to a palindrome"
