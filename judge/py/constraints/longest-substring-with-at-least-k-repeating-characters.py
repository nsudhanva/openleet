"""Longest Substring with At Least K Repeating Characters: a lowercase string and k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all(c.isascii() and c.isalpha() and c.islower() for c in s), (
        "s consists of only lowercase English letters"
    )
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
