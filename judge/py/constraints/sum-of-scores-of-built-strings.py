"""Sum of Scores of Built Strings: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert s.isascii() and s.isalpha() and s.islower(), "s consists of lowercase English letters"
