"""Longest String Chain: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    assert all(1 <= len(w) <= 16 for w in words), "1 <= words[i].length <= 16"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] only consists of lowercase English letters"
    )
