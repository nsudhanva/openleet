"""Decrypt String from Alphabet to Integer Mapping: digits and '#' encoding a-z."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(c in "0123456789#" for c in s), "s consists of digits and '#'"
    j = len(s) - 1
    while j >= 0:
        if s[j] == "#":
            assert j >= 2 and s[j - 2 : j].isdigit(), "s is a valid string"
            assert 10 <= int(s[j - 2 : j]) <= 26, "'#' follows 10 to 26"
            j -= 3
        else:
            assert s[j] != "0", "s is a valid string such that mapping is always possible"
            j -= 1
