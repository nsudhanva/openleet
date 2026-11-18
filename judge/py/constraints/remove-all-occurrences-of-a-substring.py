"""Remove All Occurrences of a Substring: lowercase strings s and part."""


def check(s: str, part: str) -> None:
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert 1 <= len(part) <= 1000, "1 <= part.length <= 1000"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
    assert all("a" <= c <= "z" for c in part), "part consists of lowercase English letters"
