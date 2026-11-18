"""Time Needed to Rearrange a Binary String: a binary string."""


def check(s: str) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(c in "01" for c in s), "s[i] is either '0' or '1'"
