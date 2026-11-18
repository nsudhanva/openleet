"""Number of Substrings With Only 1s: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert set(s) <= {"0", "1"}, "s[i] is either '0' or '1'"
