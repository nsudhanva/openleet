"""Complex Number Multiplication: two complex numbers as "real+imaginaryi" strings."""

import re


def check(num1: str, num2: str) -> None:
    for name, s in (("num1", num1), ("num2", num2)):
        assert isinstance(s, str), f"{name} is a string"
        m = re.fullmatch(r"(-?[0-9]+)\+(-?[0-9]+)i", s)
        assert m, f"{name} is a valid complex number"
        assert -100 <= int(m.group(1)) <= 100, "real is in [-100, 100]"
        assert -100 <= int(m.group(2)) <= 100, "imaginary is in [-100, 100]"
