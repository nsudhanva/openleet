"""Find the Difference: two strings, t is s shuffled plus one letter."""

from collections import Counter


def check(s: str, t: str) -> None:
    assert isinstance(s, str) and isinstance(t, str), "s and t are strings"
    assert 0 <= len(s) <= 1000, "0 <= s.length <= 1000"
    assert len(t) == len(s) + 1, "t.length == s.length + 1"
    assert all("a" <= c <= "z" for c in s + t), "s and t consist of lowercase English letters"
    extra = Counter(t)
    extra.subtract(Counter(s))
    assert all(c >= 0 for c in extra.values()) and sum(extra.values()) == 1, (
        "t is s shuffled plus one added letter"
    )
