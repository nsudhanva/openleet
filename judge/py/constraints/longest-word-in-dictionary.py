"""Longest Word in Dictionary: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    assert all(1 <= len(w) <= 30 for w in words), "1 <= words[i].length <= 30"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists of lowercase English letters"
    )
