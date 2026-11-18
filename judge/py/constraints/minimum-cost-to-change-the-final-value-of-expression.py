"""Minimum Cost to Change the Final Value of Expression: a valid boolean expression string."""


def check(expression: str) -> None:
    assert isinstance(expression, str), "expression is a string"
    assert 1 <= len(expression) <= 10**5, "1 <= expression.length <= 10^5"
    assert all(c in "10&|()" for c in expression), "expression only contains 1, 0, &, |, ( and )"
    depth = 0
    want_operand = True
    for c in expression:
        if want_operand:
            if c == "(":
                depth += 1
            else:
                assert c in "01", "a valid expression: operand expected"
                want_operand = False
        elif c in "&|":
            want_operand = True
        else:
            assert c == ")", "a valid expression: operator or ')' expected"
            depth -= 1
            assert depth >= 0, "all parentheses are properly matched"
    assert not want_operand, "a valid expression: ends with an operand"
    assert depth == 0, "all parentheses are properly matched"
