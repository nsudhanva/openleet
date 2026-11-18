"""Ternary Expression Parser: a valid ternary expression with one-digit numbers."""


def check(expression: str) -> None:
    assert isinstance(expression, str), "expression is a string"
    n = len(expression)
    assert 5 <= n <= 10**4, "5 <= expression.length <= 10^4"
    assert set(expression) <= set("0123456789TF?:"), (
        "expression consists of digits, 'T', 'F', '?', and ':'"
    )
    for i, c in enumerate(expression):
        if c not in "?:":
            assert i == n - 1 or expression[i + 1] in "?:", "each number is a one-digit number"
            assert i == 0 or expression[i - 1] in "?:", "each number is a one-digit number"
    # valid ternary expression: evaluate right to left
    stack: list[str] = []
    i = n - 1
    while i >= 0:
        c = expression[i]
        if c == ":":
            i -= 1
        elif c == "?":
            assert i >= 1 and expression[i - 1] in "TF", "valid ternary expression"
            assert len(stack) >= 2, "valid ternary expression"
            yes, no = stack.pop(), stack.pop()
            stack.append(yes if expression[i - 1] == "T" else no)
            i -= 2
        else:
            stack.append(c)
            i -= 1
    assert len(stack) == 1, "valid ternary expression"
