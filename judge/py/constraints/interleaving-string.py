"""Interleaving String: three lowercase strings s1, s2, s3."""


def check(s1: str, s2: str, s3: str) -> None:
    assert all(isinstance(s, str) for s in (s1, s2, s3)), "s1, s2, s3 are strings"
    assert 0 <= len(s1) <= 100, "0 <= s1.length <= 100"
    assert 0 <= len(s2) <= 100, "0 <= s2.length <= 100"
    assert 0 <= len(s3) <= 200, "0 <= s3.length <= 200"
    for s in (s1, s2, s3):
        assert all("a" <= c <= "z" for c in s), "s1, s2, s3 are lowercase English letters"
