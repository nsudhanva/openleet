"""Minimum Number of Changes to Make Binary String Beautiful: an even-length binary string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 2 <= len(s) <= 10**5, "2 <= s.length <= 10^5"
    assert len(s) % 2 == 0, "s has an even length"
    assert all(c in "01" for c in s), "s[i] is either '0' or '1'"
