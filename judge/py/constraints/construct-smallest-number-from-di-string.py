"""Construct Smallest Number From DI String: a pattern of 'I' and 'D'."""


def check(pattern: str) -> None:
    assert 1 <= len(pattern) <= 8, "1 <= pattern.length <= 8"
    assert all(c in "ID" for c in pattern), "pattern consists of only the letters 'I' and 'D'"
