"""Minimum Remove to Make Valid Parentheses: a string of parentheses and lowercase letters."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "()" or "a" <= c <= "z" for c in s), (
        "s[i] is either '(' , ')', or lowercase English letter"
    )
