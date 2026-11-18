"""Reverse String Prefix: a lowercase string and a prefix length k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
    assert 1 <= k <= len(s), "1 <= k <= s.length"
