"""Orderly Queue: a lowercase string s and k, the number of leading characters that can be moved."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= k <= len(s) <= 1000, "1 <= k <= s.length <= 1000"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
