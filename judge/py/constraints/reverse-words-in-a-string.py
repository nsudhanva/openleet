"""Reverse Words in a String: letters, digits and spaces with at least one word."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert all(c == " " or (c.isascii() and c.isalnum()) for c in s), (
        "s contains English letters, digits, and spaces"
    )
    assert s.strip(" ") != "", "there is at least one word in s"
