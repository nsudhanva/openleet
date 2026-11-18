"""Minimum Insertions to Balance a Parentheses String: a string of '(' and ')'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "()" for c in s), "s consists of '(' and ')' only"
