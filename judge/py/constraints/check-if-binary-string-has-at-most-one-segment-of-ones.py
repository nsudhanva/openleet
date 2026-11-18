"""Check if Binary String Has at Most One Segment of Ones: a binary string starting with 1."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert set(s) <= {"0", "1"}, "s[i] is either '0' or '1'"
    assert s[0] == "1", "s[0] is '1'"
