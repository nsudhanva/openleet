"""Make The String Great: a string of upper and lower case English letters."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c.isascii() and c.isalpha() for c in s), "only English letters"
