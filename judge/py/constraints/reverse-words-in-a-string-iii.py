"""Reverse Words in a String III: printable ASCII words separated by single spaces."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 5 * 10**4, "1 <= s.length <= 5 * 10^4"
    assert all(32 <= ord(c) <= 126 for c in s), "s contains printable ASCII characters"
    assert s.strip(" ") != "", "there is at least one word in s"
    assert s[0] != " " and s[-1] != " ", "s does not contain any leading or trailing spaces"
    assert "  " not in s, "all the words in s are separated by a single space"
