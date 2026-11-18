"""Longest Balanced Substring After One Swap: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "01" for c in s), "s consists only of the characters '0' and '1'"
