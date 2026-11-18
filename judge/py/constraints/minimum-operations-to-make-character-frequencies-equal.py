"""Minimum Operations to Make Character Frequencies Equal: a lowercase string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 3 <= len(s) <= 2 * 10**4, "3 <= s.length <= 2 * 10^4"
    assert all("a" <= c <= "z" for c in s), "s contains only lowercase English letters"
