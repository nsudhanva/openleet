"""Smallest Substring With Identical Characters I: a binary string and numOps."""


def check(s: str, numOps: int) -> None:
    assert 1 <= len(s) <= 1000, "1 <= n == s.length <= 1000"
    assert all(c in "01" for c in s), "s consists only of '0' and '1'"
    assert 0 <= numOps <= len(s), "0 <= numOps <= n"
