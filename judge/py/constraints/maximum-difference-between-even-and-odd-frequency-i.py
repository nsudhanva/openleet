"""Maximum Difference Between Even and Odd Frequency I: a lowercase string."""

from collections import Counter


def check(s: str) -> None:
    assert 3 <= len(s) <= 100, "3 <= s.length <= 100"
    assert all("a" <= c <= "z" for c in s), "s consists only of lowercase English letters"
    counts = Counter(s).values()
    assert any(c % 2 == 1 for c in counts), "s has a character with an odd frequency"
    assert any(c % 2 == 0 for c in counts), "s has a character with an even frequency"
