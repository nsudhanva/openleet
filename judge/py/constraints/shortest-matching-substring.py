"""Shortest Matching Substring: a lowercase string and a pattern with exactly two '*'."""


def check(s: str, p: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert 2 <= len(p) <= 10**5, "2 <= p.length <= 10^5"
    assert all("a" <= ch <= "z" for ch in s), "s contains only lowercase English letters"
    assert all(ch == "*" or "a" <= ch <= "z" for ch in p), (
        "p contains only lowercase English letters and '*'"
    )
    assert p.count("*") == 2, "p contains exactly two '*'"
