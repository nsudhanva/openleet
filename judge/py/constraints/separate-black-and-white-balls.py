"""Separate Black and White Balls: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 10**5, "1 <= n == s.length <= 10^5"
    assert set(s) <= {"0", "1"}, "s[i] is either '0' or '1'"
