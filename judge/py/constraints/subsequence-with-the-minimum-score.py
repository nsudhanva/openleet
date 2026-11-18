"""Subsequence With the Minimum Score: two lowercase strings s and t."""


def check(s: str, t: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert 1 <= len(t) <= 10**5, "1 <= t.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
    assert all("a" <= c <= "z" for c in t), "t consists of lowercase English letters"
