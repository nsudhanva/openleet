"""Basic Calculator IV: an expression, variable names to evaluate and their values."""

import re


def check(expression: str, evalvars: list[str], evalints: list[int]) -> None:
    assert isinstance(expression, str), "expression is a string"
    assert 1 <= len(expression) <= 250, "1 <= expression.length <= 250"
    assert set(expression) <= set("abcdefghijklmnopqrstuvwxyz0123456789+-*() "), (
        "expression consists of lowercase English letters, digits, '+', '-', '*', '(', ')', ' '"
    )
    assert expression == expression.strip(" "), "no leading or trailing spaces"
    assert "  " not in expression, "all the tokens in expression are separated by a single space"
    assert len(evalvars) == len(evalints), "evalints.length == evalvars.length"
    assert 0 <= len(evalvars) <= 100, "0 <= evalvars.length <= 100"
    assert all(isinstance(v, str) and 1 <= len(v) <= 20 for v in evalvars), (
        "1 <= evalvars[i].length <= 20"
    )
    assert all(re.fullmatch(r"[a-z]+", v) for v in evalvars), "evalvars[i] is lowercase letters"
    assert all(-100 <= v <= 100 for v in evalints), "-100 <= evalints[i] <= 100"
    # grammar: chunks (parenthesised expression, variable, non-negative integer) joined by + - *
    tokens = re.findall(r"[a-z]+|\d+|[-+*()]", expression.replace(" ", ""))
    assert "".join(tokens) == expression.replace(" ", ""), "expression is valid"
    operand = True
    depth = 0
    for t in tokens:
        if t == "(":
            assert operand, "expression is valid"
            depth += 1
        elif t == ")":
            assert not operand and depth > 0, "expression is valid"
            depth -= 1
        elif t in "+-*":
            assert not operand, "an expression alternates chunks and symbols"
            operand = True
        else:
            assert operand, "an expression alternates chunks and symbols"
            operand = False
    assert not operand and depth == 0, "expression is valid"
