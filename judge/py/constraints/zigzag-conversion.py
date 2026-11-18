"""Zigzag Conversion: a string of letters, ',' and '.', and a row count."""

import string


def check(s: str, numRows: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    allowed = set(string.ascii_letters + ",.")
    assert all(c in allowed for c in s), "s consists of English letters, ',' and '.'"
    assert 1 <= numRows <= 1000, "1 <= numRows <= 1000"
