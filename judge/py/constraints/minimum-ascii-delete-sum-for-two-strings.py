"""Minimum ASCII Delete Sum for Two Strings: two lowercase strings."""


def check(s1: str, s2: str) -> None:
    assert isinstance(s1, str) and isinstance(s2, str), "s1 and s2 are strings"
    assert 1 <= len(s1) <= 1000, "1 <= s1.length <= 1000"
    assert 1 <= len(s2) <= 1000, "1 <= s2.length <= 1000"
    assert all("a" <= c <= "z" for c in s1 + s2), "s1 and s2 consist of lowercase English letters"
