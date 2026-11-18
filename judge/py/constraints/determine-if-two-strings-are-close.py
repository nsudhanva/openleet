"""Determine if Two Strings Are Close: two lowercase strings."""


def check(word1: str, word2: str) -> None:
    for w in (word1, word2):
        assert isinstance(w, str) and 1 <= len(w) <= 10**5, "1 <= word.length <= 10^5"
        assert all("a" <= c <= "z" for c in w), "word contains only lowercase English letters"
