"""Subsequence After One Replacement: two lowercase strings."""


def check(s: str, t: str) -> None:
    assert isinstance(s, str) and isinstance(t, str), "s and t are strings"
    assert 1 <= len(s) <= 10**5 and 1 <= len(t) <= 10**5, "1 <= s.length, t.length <= 10^5"
    assert all("a" <= c <= "z" for c in s + t), "s and t consist only of lowercase English letters"
