"""Maximum Odd Binary Number: a binary string with at least one '1'."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c in "01" for c in s), "s consists only of '0' and '1'"
    assert "1" in s, "s contains at least one '1'"
