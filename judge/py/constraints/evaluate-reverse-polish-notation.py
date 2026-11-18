"""Evaluate Reverse Polish Notation: tokens of a valid RPN expression."""

import re

_INT = re.compile(r"-?[0-9]+")


def check(tokens: list[str]) -> None:
    assert isinstance(tokens, list), "list"
    assert 1 <= len(tokens) <= 10**4, "1 <= tokens.length <= 10^4"
    lim = 2**31
    stack: list[int] = []
    for t in tokens:
        assert isinstance(t, str), "tokens are strings"
        if t in ("+", "-", "*", "/"):
            assert len(stack) >= 2, "the input is a valid reverse polish expression"
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                r = a + b
            elif t == "-":
                r = a - b
            elif t == "*":
                r = a * b
            else:
                assert b != 0, "there will not be any division by zero"
                q = abs(a) // abs(b)
                r = q if (a >= 0) == (b >= 0) else -q
            assert -lim <= r < lim, "intermediate calculations fit in a 32-bit integer"
            stack.append(r)
        else:
            assert _INT.fullmatch(t), "tokens[i] is an operator or an integer"
            assert -200 <= int(t) <= 200, "integer tokens are in the range [-200, 200]"
            stack.append(int(t))
    assert len(stack) == 1, "the input is a valid reverse polish expression"
