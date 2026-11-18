"""Fraction Addition and Subtraction: 1 to 10 irreducible fractions joined by + and -."""

import re
from fractions import Fraction
from math import gcd


def check(expression: str) -> None:
    assert re.fullmatch(r"[0-9/+\-]+", expression), "only '0'-'9', '/', '+' and '-'"
    assert re.fullmatch(r"-?\d+/\d+([+-]\d+/\d+)*", expression), "format ±numerator/denominator"
    terms = re.findall(r"([+-]?)(\d+)/(\d+)", expression)
    assert 1 <= len(terms) <= 10, "1 to 10 fractions"
    total = Fraction(0)
    for sign, a, b in terms:
        num, den = int(a), int(b)
        assert 1 <= num <= 10 and 1 <= den <= 10, "numerator and denominator in [1, 10]"
        assert gcd(num, den) == 1, "each fraction is irreducible"
        total += -Fraction(num, den) if sign == "-" else Fraction(num, den)
    assert abs(total.numerator) < 2**31 and total.denominator < 2**31, "result fits in 32-bit int"
