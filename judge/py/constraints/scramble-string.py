"""Scramble String: two lowercase strings of equal length."""


def check(s1: str, s2: str) -> None:
    assert len(s1) == len(s2), "s1.length == s2.length"
    assert 1 <= len(s1) <= 30, "1 <= s1.length <= 30"
    assert all("a" <= c <= "z" for c in s1 + s2), "s1 and s2 consist of lowercase English letters"
