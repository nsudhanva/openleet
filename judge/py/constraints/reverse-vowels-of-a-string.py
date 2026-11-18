"""Reverse Vowels of a String: a string of printable ASCII characters."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 3 * 10**5, "1 <= s.length <= 3 * 10^5"
    assert all(32 <= ord(c) <= 126 for c in s), "s consists of printable ASCII characters"
