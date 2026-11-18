"""Shortest Distance to a Character: a lowercase string and a lowercase character in it."""


def check(s: str, c: str) -> None:
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all("a" <= ch <= "z" for ch in s), "s[i] is a lowercase English letter"
    assert len(c) == 1 and "a" <= c <= "z", "c is a lowercase English letter"
    assert c in s, "c occurs at least once in s"
