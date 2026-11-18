"""Substring Matching Pattern: a lowercase string and a pattern with exactly one '*'."""


def check(s: str, p: str) -> None:
    assert 1 <= len(s) <= 50, "1 <= s.length <= 50"
    assert 1 <= len(p) <= 50, "1 <= p.length <= 50"
    assert all("a" <= c <= "z" for c in s), "s contains only lowercase English letters"
    assert p.count("*") == 1, "p contains exactly one '*'"
    assert all(c == "*" or "a" <= c <= "z" for c in p), (
        "p contains only lowercase English letters and '*'"
    )
