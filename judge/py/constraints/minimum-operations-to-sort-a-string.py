"""Minimum Operations to Sort a String: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" and len(c) == 1 for c in s), (
        "s consists of only lowercase English letters"
    )
