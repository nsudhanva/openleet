"""Minimum Number of Steps to Make Two Strings Anagram: two equal-length lowercase strings."""


def check(s: str, t: str) -> None:
    assert isinstance(s, str) and isinstance(t, str), "s and t are strings"
    assert 1 <= len(s) <= 5 * 10**4, "1 <= s.length <= 5 * 10^4"
    assert len(s) == len(t), "s.length == t.length"
    assert all("a" <= c <= "z" and len(c) == 1 for c in s + t), (
        "s and t consist of lowercase English letters only"
    )
