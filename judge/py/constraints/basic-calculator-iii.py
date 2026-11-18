"""Basic Calculator III: non-negative integers, '+', '-', '*', '/' and parentheses."""

LIMIT = 2**31


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert set(s) <= set("0123456789+-*/()"), "s consists of digits, + - * / ( )"
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    vals: list[int] = []
    ops: list[str] = []

    def apply() -> None:
        op = ops.pop()
        b = vals.pop()
        a = vals.pop()
        if op == "+":
            r = a + b
        elif op == "-":
            r = a - b
        elif op == "*":
            r = a * b
        else:
            assert b != 0, "s is a valid expression (no division by zero)"
            r = abs(a) // abs(b) * (1 if (a >= 0) == (b >= 0) else -1)
        assert -LIMIT <= r < LIMIT, "all intermediate results are in the range [-2^31, 2^31 - 1]"
        vals.append(r)

    operand = True
    depth = 0
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isdigit():
            assert operand, "s is a valid expression"
            j = i
            while j < n and s[j].isdigit():
                j += 1
            v = int(s[i:j])
            assert v < LIMIT, "all intermediate results are in the range [-2^31, 2^31 - 1]"
            vals.append(v)
            operand = False
            i = j
            continue
        if c == "(":
            assert operand, "s is a valid expression"
            depth += 1
            ops.append(c)
        elif c == ")":
            assert not operand and depth > 0, "s is a valid expression"
            depth -= 1
            while ops[-1] != "(":
                apply()
            ops.pop()
        else:
            assert not operand, "s is a valid expression"
            while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[c]:
                apply()
            ops.append(c)
            operand = True
        i += 1
    assert not operand and depth == 0, "s is a valid expression"
    while ops:
        apply()
