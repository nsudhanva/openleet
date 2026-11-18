"""Count Anagrams: a string of lowercase words separated by single spaces."""


def check(s: str) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c == " " or "a" <= c <= "z" for c in s), (
        "s consists of lowercase English letters and spaces"
    )
    assert "  " not in s, "There is single space between consecutive words"
    assert s.strip(" ") == s and s != "", (
        "s contains one or more words, so no leading or trailing space"
    )
