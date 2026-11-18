"""Number of Ways to Select Buildings: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 3 <= len(s) <= 10**5, "3 <= s.length <= 10^5"
    assert set(s) <= {"0", "1"}, "s[i] is either '0' or '1'"
