"""Isomorphic Strings: two ASCII strings of equal length."""


def check(s: str, t: str) -> None:
    assert isinstance(s, str) and isinstance(t, str), "s and t are strings"
    assert 1 <= len(s) <= 5 * 10**4, "1 <= s.length <= 5 * 10^4"
    assert len(t) == len(s), "t.length == s.length"
    assert s.isascii() and t.isascii(), "s and t consist of valid ASCII characters"
