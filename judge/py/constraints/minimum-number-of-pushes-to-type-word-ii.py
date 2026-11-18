"""Minimum Number of Pushes to Type Word II: a lowercase word."""


def check(word: str) -> None:
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 10**5, "1 <= word.length <= 10^5"
    assert all("a" <= c <= "z" and len(c) == 1 for c in word), (
        "word consists of lowercase English letters"
    )
