"""Student Attendance Record I: a string of A, L, P."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(c in "ALP" for c in s), "s[i] is either 'A', 'L', or 'P'"
