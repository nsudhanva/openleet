"""Longest Ideal Subsequence: a lowercase string and a difference bound k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert 0 <= k <= 25, "0 <= k <= 25"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
