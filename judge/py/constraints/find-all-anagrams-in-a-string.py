"""Find All Anagrams in a String: two lowercase strings s and p."""


def check(s: str, p: str) -> None:
    assert isinstance(s, str) and isinstance(p, str), "s and p are strings"
    assert 1 <= len(s) <= 3 * 10**4, "1 <= s.length <= 3 * 10^4"
    assert 1 <= len(p) <= 3 * 10**4, "1 <= p.length <= 3 * 10^4"
    assert all(c.isascii() and c.islower() and c.isalpha() for c in s + p), (
        "s and p consist of lowercase English letters"
    )
