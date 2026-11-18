"""Generalized Abbreviation: a lowercase word."""


def check(word: str) -> None:
    assert 1 <= len(word) <= 15, "1 <= word.length <= 15"
    assert all("a" <= c <= "z" for c in word), "word consists of only lowercase English letters"
