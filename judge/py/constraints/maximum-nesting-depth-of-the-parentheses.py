"""Maximum Nesting Depth of the Parentheses: a valid parentheses string with digits and
operators."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c in "0123456789+-*/()" for c in s), "s consists of digits and '+-*/()'"
    depth = 0
    for c in s:
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            assert depth >= 0, "s is a VPS"
    assert depth == 0, "s is a VPS"
