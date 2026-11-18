"""Determine if String Halves Are Alike: an even-length string of letters."""


def check(s: str) -> None:
    assert isinstance(s, str) and 2 <= len(s) <= 1000, "2 <= s.length <= 1000"
    assert len(s) % 2 == 0, "s.length is even"
    assert s.isascii() and s.isalpha(), "s consists of uppercase and lowercase letters"
