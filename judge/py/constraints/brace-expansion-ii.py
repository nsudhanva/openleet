"""Brace Expansion II: an expression of letters, braces and commas under the stated grammar."""

from string import ascii_lowercase

_LOWER = set(ascii_lowercase)


def check(expression: str) -> None:
    assert 1 <= len(expression) <= 60, "1 <= expression.length <= 60"
    assert set(expression) <= _LOWER | set("{},"), (
        "expression[i] is '{', '}', ',' or a lowercase letter"
    )
    # frames hold [commas seen, current term non-empty]; the base frame is the whole expression
    stack = [[0, False]]
    for c in expression:
        top = stack[-1]
        if c == "{":
            stack.append([0, False])
        elif c == ",":
            assert len(stack) > 1, "a comma-delimited list sits inside braces"
            assert top[1], "every expression in a list is non-empty"
            top[0] += 1
            top[1] = False
        elif c == "}":
            assert len(stack) > 1, "braces are balanced"
            assert top[1], "every expression in a list is non-empty"
            assert top[0] >= 1, "a comma-delimited list has k >= 2 expressions"
            stack.pop()
            stack[-1][1] = True
        else:
            top[1] = True
    assert len(stack) == 1, "braces are balanced"
    assert stack[0][1], "expression is a valid expression of the grammar"
