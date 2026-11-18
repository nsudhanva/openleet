"""Minimum Operations to Equalize Binary String: a binary string and a flip size k."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert set(s) <= {"0", "1"}, "s[i] is either '0' or '1'"
    assert 1 <= k <= len(s), "1 <= k <= s.length"
