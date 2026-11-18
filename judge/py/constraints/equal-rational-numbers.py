"""Equal Rational Numbers: two non-negative rationals with an optional repeating part."""

import re

_FORM = re.compile(r"(0|[1-9][0-9]{0,3})(?:\.([0-9]{0,4})(?:\(([0-9]{1,4})\))?)?")


def check(s: str, t: str) -> None:
    for name, x in (("s", s), ("t", t)):
        assert isinstance(x, str), f"{name} is a string"
        assert _FORM.fullmatch(x), (
            f"{name}: <IntegerPart>[.<NonRepeatingPart>[(<RepeatingPart>)]], digits only, "
            "integer part without leading zeros and 1-4 digits, non-repeating part 0-4 digits, "
            "repeating part 1-4 digits"
        )
