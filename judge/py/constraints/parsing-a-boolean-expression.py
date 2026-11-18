"""Parsing A Boolean Expression: a valid expression built from t, f, !(), &() and |()."""


def check(expression: str) -> None:
    assert isinstance(expression, str), "expression is a string"
    assert 1 <= len(expression) <= 2 * 10**4, "1 <= expression.length <= 2 * 10^4"
    assert all(c in "()&|!tf," for c in expression), "expression[i] is one of ( ) & | ! t f ,"
    stack: list[list] = []  # [operator, completed sub-expressions]
    expect = True  # an expression must start at the next character
    done = False
    i, n = 0, len(expression)
    while i < n:
        c = expression[i]
        assert not done, "the expression is valid"
        if c in "tf":
            assert expect, "the expression is valid"
            expect = False
            if stack:
                stack[-1][1] += 1
            else:
                done = True
        elif c in "&|!":
            assert expect and i + 1 < n and expression[i + 1] == "(", "the expression is valid"
            stack.append([c, 0])
            i += 1
        elif c == ",":
            assert not expect and stack and stack[-1][0] != "!", "the expression is valid"
            expect = True
        elif c == ")":
            assert not expect and stack, "the expression is valid"
            stack.pop()
            if stack:
                stack[-1][1] += 1
            else:
                done = True
        else:
            raise AssertionError("the expression is valid")
        i += 1
    assert done and not stack, "the expression is valid"
