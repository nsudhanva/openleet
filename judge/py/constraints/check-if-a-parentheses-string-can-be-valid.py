"""Check if a Parentheses String Can Be Valid: a parentheses string and a lock mask."""


def check(s: str, locked: str) -> None:
    assert isinstance(s, str) and isinstance(locked, str), "s, locked are strings"
    assert len(s) == len(locked), "n == s.length == locked.length"
    assert 1 <= len(s) <= 10**5, "1 <= n <= 10^5"
    assert all(c in "()" for c in s), "s[i] is either '(' or ')'"
    assert all(c in "01" for c in locked), "locked[i] is either '0' or '1'"
