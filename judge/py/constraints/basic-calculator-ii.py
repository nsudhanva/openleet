"""Basic Calculator II: non-negative integers and '+', '-', '*', '/' separated by spaces."""

import re


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 3 * 10**5, "1 <= s.length <= 3 * 10^5"
    assert set(s) <= set("0123456789+-*/ "), "s consists of integers, '+', '-', '*', '/' and spaces"
    tokens = re.findall(r"\d+|[-+*/]", s)
    assert len(tokens) % 2 == 1, "s represents a valid expression"
    for i, t in enumerate(tokens):
        assert t.isdigit() == (i % 2 == 0), "s represents a valid expression"
    nums = [int(t) for t in tokens[::2]]
    assert all(0 <= v <= 2**31 - 1 for v in nums), "all the integers are in the range [0, 2^31 - 1]"
    total = 0
    term = nums[0]
    for op, v in zip(tokens[1::2], nums[1:], strict=True):
        if op == "*":
            term *= v
        elif op == "/":
            assert v != 0, "s represents a valid expression (no division by zero)"
            term = abs(term) // v * (1 if term >= 0 else -1)
        else:
            total += term
            term = v if op == "+" else -v
    total += term
    assert -(2**31) <= total <= 2**31 - 1, "the answer fits in a 32-bit integer"
