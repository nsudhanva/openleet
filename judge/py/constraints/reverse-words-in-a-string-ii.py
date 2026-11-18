"""Reverse Words in a String II: a character array of single-space-separated words."""


def check(s: list[str]) -> None:
    assert isinstance(s, list), "s is a list"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(isinstance(c, str) and len(c) == 1 for c in s), "s[i] is a single character"
    assert all(c == " " or (c.isascii() and c.isalnum()) for c in s), (
        "s[i] is an English letter, digit, or space"
    )
    assert any(c != " " for c in s), "there is at least one word in s"
    assert s[0] != " " and s[-1] != " ", "s does not contain leading or trailing spaces"
    assert all(not (s[i] == " " and s[i + 1] == " ") for i in range(len(s) - 1)), (
        "words are separated by a single space"
    )
