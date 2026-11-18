"""Roman to Integer: a valid roman numeral for 1..3999."""

import re

_VALID = re.compile(r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})")


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 15, "1 <= s.length <= 15"
    assert all(c in "IVXLCDM" for c in s), "s contains only I, V, X, L, C, D, M"
    assert _VALID.fullmatch(s), "s is a valid roman numeral in the range [1, 3999]"
