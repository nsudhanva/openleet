"""Is Subsequence: two lowercase strings s and t."""


def check(s: str, t: str) -> None:
    assert isinstance(s, str) and isinstance(t, str), "s and t are strings"
    assert 0 <= len(s) <= 100, "0 <= s.length <= 100"
    assert 0 <= len(t) <= 10**4, "0 <= t.length <= 10^4"
    assert all("a" <= c <= "z" for c in s + t), "s and t consist only of lowercase English letters"
