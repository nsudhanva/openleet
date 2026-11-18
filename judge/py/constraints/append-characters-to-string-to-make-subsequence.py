"""Append Characters to String to Make Subsequence: two lowercase strings."""


def check(s: str, t: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert 1 <= len(t) <= 10**5, "1 <= t.length <= 10^5"
    assert all("a" <= c <= "z" for c in s + t), "s and t consist only of lowercase English letters"
