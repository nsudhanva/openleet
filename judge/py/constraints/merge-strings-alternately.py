"""Merge Strings Alternately: two lowercase words."""


def check(word1: str, word2: str) -> None:
    for w in (word1, word2):
        assert 1 <= len(w) <= 100, "1 <= word.length <= 100"
        assert all("a" <= c <= "z" for c in w), "lowercase English letters"
