"""Vowels of All Substrings: a lowercase word."""


def check(word: str) -> None:
    assert 1 <= len(word) <= 10**5, "1 <= word.length <= 10^5"
    assert word.isascii() and word.isalpha() and word.islower(), (
        "word consists of lowercase English letters"
    )
