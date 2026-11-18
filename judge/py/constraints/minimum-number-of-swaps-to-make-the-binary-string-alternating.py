"""Minimum Number of Swaps to Make the Binary String Alternating: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert set(s) <= {"0", "1"}, "s[i] is either '0' or '1'"
