"""Different Ways to Add Parentheses: an expression of numbers and + - *."""

import re


def check(expression: str) -> None:
    assert isinstance(expression, str) and 1 <= len(expression) <= 20, (
        "1 <= expression.length <= 20"
    )
    assert re.fullmatch(r"[0-9+\-*]+", expression), (
        "expression consists of digits and '+', '-', '*'"
    )
    assert re.fullmatch(r"[0-9]+([+\-*][0-9]+)*", expression), (
        "numbers have no sign and operators sit between numbers"
    )
    assert all(int(x) <= 99 for x in re.split(r"[+\-*]", expression)), (
        "integer values are in [0, 99]"
    )
