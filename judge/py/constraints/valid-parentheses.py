"""Valid Parentheses: a string of bracket characters."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all(c in "()[]{}" for c in s), "s consists of parentheses only '()[]{}'"
