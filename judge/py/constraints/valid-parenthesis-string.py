"""Valid Parenthesis String: a string of '(', ')' and '*'."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c in "()*" for c in s), "s[i] is '(', ')' or '*'"
