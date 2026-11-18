"""Longest Valid Parentheses: a string of parentheses."""


def check(s: str) -> None:
    assert 0 <= len(s) <= 3 * 10**4, "0 <= s.length <= 3 * 10^4"
    assert all(c in "()" for c in s), "s[i] is '(' or ')'"
