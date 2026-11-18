"""Remove Outermost Parentheses: a valid parentheses string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "()" for c in s), "s[i] is either '(' or ')'"
    depth = 0
    for c in s:
        depth += 1 if c == "(" else -1
        assert depth >= 0, "s is a valid parentheses string"
    assert depth == 0, "s is a valid parentheses string"
