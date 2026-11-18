"""Vowels Game in a String: a lowercase string."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert s.isascii() and s.isalpha() and s.islower(), (
        "s consists only of lowercase English letters"
    )
