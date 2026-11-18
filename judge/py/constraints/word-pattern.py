"""Word Pattern: a lowercase pattern and a string of lowercase words separated by single spaces."""


def check(pattern: str, s: str) -> None:
    assert 1 <= len(pattern) <= 300, "1 <= pattern.length <= 300"
    assert all("a" <= c <= "z" for c in pattern), "pattern contains only lower-case English letters"
    assert 1 <= len(s) <= 3000, "1 <= s.length <= 3000"
    assert all("a" <= c <= "z" or c == " " for c in s), (
        "s contains only lowercase English letters and spaces"
    )
    assert s == s.strip(" "), "s does not contain any leading or trailing spaces"
    assert "  " not in s, "all the words in s are separated by a single space"
