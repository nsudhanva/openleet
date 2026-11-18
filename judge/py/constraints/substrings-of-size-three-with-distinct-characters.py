"""Substrings of Size Three with Distinct Characters: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
