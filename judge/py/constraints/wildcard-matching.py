"""Wildcard Matching: a lowercase string and a pattern of lowercase letters, ? and *."""


def check(s: str, p: str) -> None:
    assert 0 <= len(s) <= 2000, "0 <= s.length <= 2000"
    assert 0 <= len(p) <= 2000, "0 <= p.length <= 2000"
    assert all("a" <= c <= "z" for c in s), "s contains only lowercase English letters"
    assert all("a" <= c <= "z" or c in "?*" for c in p), (
        "p contains only lowercase English letters, '?' or '*'"
    )
