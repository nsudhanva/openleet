"""Longest Nice Substring: a string of English letters."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all(c.isascii() and c.isalpha() for c in s), (
        "s consists of uppercase and lowercase English letters"
    )
