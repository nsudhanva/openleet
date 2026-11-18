"""DI String Match: a string of I and D."""


def check(s: str) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert set(s) <= {"I", "D"}, "s[i] is either 'I' or 'D'"
