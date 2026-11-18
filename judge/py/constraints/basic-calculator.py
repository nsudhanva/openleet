"""Basic Calculator: an expression of digits, '+', '-', parentheses and spaces."""

LIMIT = 2**31


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 3 * 10**5, "1 <= s.length <= 3 * 10^5"
    assert set(s) <= set("0123456789+-() "), "s consists of digits, '+', '-', '(', ')', and ' '"
    # state: expecting an operand (True) or an operator (False)
    operand = True
    unary_ok = True  # a '-' may be unary at the start or right after '('
    depth = 0
    result, sign = 0, 1
    stack: list[tuple[int, int]] = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == " ":
            i += 1
        elif c.isdigit():
            assert operand, "s represents a valid expression"
            j = i
            while j < n and s[j].isdigit():
                j += 1
            num = int(s[i:j])
            assert -LIMIT <= num < LIMIT, "every number fits in a signed 32-bit integer"
            result += sign * num
            assert -LIMIT <= result < LIMIT, "running calculation fits in 32 bits"
            operand, unary_ok = False, False
            i = j
        elif c == "(":
            assert operand, "s represents a valid expression"
            stack.append((result, sign))
            result, sign = 0, 1
            depth += 1
            unary_ok = True
            i += 1
        elif c == ")":
            assert not operand and depth > 0, "s represents a valid expression"
            prev, prev_sign = stack.pop()
            result = prev + prev_sign * result
            assert -LIMIT <= result < LIMIT, "running calculation fits in 32 bits"
            depth -= 1
            i += 1
        elif c == "+":
            assert not operand, "'+' is not used as a unary operation, no two consecutive operators"
            sign, operand, unary_ok = 1, True, False
            i += 1
        else:  # '-'
            if operand:
                assert unary_ok, "no two consecutive operators"
                sign = -1
                unary_ok = False
            else:
                sign, operand, unary_ok = -1, True, False
            i += 1
    assert not operand and depth == 0, "s represents a valid expression"
