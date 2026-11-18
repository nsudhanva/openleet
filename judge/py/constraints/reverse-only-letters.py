"""Reverse Only Letters: a string of printable characters."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(33 <= ord(c) <= 122 for c in s), "ASCII values of s are in [33, 122]"
    assert '"' not in s and "\\" not in s, "s does not contain '\"' or '\\'"
