"""Score of Parentheses: a balanced parentheses string."""


def check(s: str) -> None:
    assert 2 <= len(s) <= 50, "2 <= s.length <= 50"
    assert all(c in "()" for c in s), "s consists of only '(' and ')'"
    depth = 0
    for c in s:
        depth += 1 if c == "(" else -1
        assert depth >= 0, "s is a balanced parentheses string"
    assert depth == 0, "s is a balanced parentheses string"
