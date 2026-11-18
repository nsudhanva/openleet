"""Construct String With Repeat Limit: a lowercase string and a repeat limit."""


def check(s: str, repeatLimit: int) -> None:
    assert 1 <= repeatLimit <= len(s) <= 10**5, "1 <= repeatLimit <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
