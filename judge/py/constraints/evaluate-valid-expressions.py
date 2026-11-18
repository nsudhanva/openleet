"""Evaluate Valid Expressions: a nested add/sub/mul/div expression string."""

import re

_OPS = ("add", "sub", "mul", "div")
_NUM = re.compile(r"-?\d+")
_LIMIT = 2**63


def check(expression: str) -> None:
    assert isinstance(expression, str), "expression is a string"
    n = len(expression)
    assert 1 <= n <= 10**5, "1 <= expression.length <= 10^5"
    stack: list[list] = []  # frames: [op, first_operand_or_None]
    i = 0
    result = None
    while True:
        # parse one expression starting at i
        op = expression[i : i + 3]
        if op in _OPS and expression[i + 3 : i + 4] == "(":
            stack.append([op, None])
            i += 4
            continue
        m = _NUM.match(expression, i)
        assert m, "expression is valid"
        value = int(m.group())
        i = m.end()
        # a value is complete; unwind
        while True:
            assert -_LIMIT <= value < _LIMIT, "all intermediate results fit in a long integer"
            if not stack:
                result = value
                break
            frame = stack[-1]
            if frame[1] is None:
                assert expression[i : i + 1] == ",", "expression is valid"
                frame[1] = (value,)
                i += 1
                break
            assert expression[i : i + 1] == ")", "expression is valid"
            i += 1
            a, b = frame[1][0], value
            if frame[0] == "add":
                value = a + b
            elif frame[0] == "sub":
                value = a - b
            elif frame[0] == "mul":
                value = a * b
            else:
                assert b != 0 and a % b == 0, "all divisions result in integer values"
                value = a // b
            stack.pop()
        if result is not None:
            break
    assert i == n, "expression is valid"
