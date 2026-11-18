"""Solve the Equation: a linear equation in x with integer terms."""

import re

_SIDE = re.compile(r"(?:[+-]?(?:[0-9]+x?|x))(?:[+-](?:[0-9]+x?|x))*")
_TERM = re.compile(r"([+-]?)([0-9]*)(x?)")


def check(equation: str) -> None:
    assert 3 <= len(equation) <= 1000, "3 <= equation.length <= 1000"
    assert equation.count("=") == 1, "equation has exactly one '='"
    sides = equation.split("=")
    assert all(_SIDE.fullmatch(s) for s in sides), (
        "equation consists of integers and the variable 'x' joined by + and -"
    )
    a = b = 0
    for sign_side, side in zip((1, -1), sides, strict=True):
        for sign, digits, x in _TERM.findall(side):
            if not (sign or digits or x):
                continue
            assert digits == "" or digits == "0" or not digits.startswith("0"), "no leading zeros"
            assert digits == "" or int(digits) <= 100, "absolute value in the range [0, 100]"
            v = (int(digits) if digits else 1) if x else int(digits)
            v *= sign_side * (-1 if sign == "-" else 1)
            if x:
                a += v
            else:
                b -= v
    assert a == 0 or b % a == 0, "a single solution is an integer"
