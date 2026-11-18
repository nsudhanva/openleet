"""Smallest Substring With Identical Characters II: a binary string and numOps."""


def check(s: str, numOps: int) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= n == s.length <= 10^5"
    assert all(c in "01" for c in s), "s consists only of '0' and '1'"
    assert 0 <= numOps <= len(s), "0 <= numOps <= n"
