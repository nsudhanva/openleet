"""Longest Word in Dictionary through Deleting: a lowercase string and a word list."""


def check(s: str, dictionary: list[str]) -> None:
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert 1 <= len(dictionary) <= 1000, "1 <= dictionary.length <= 1000"
    assert all(1 <= len(w) <= 1000 for w in dictionary), "1 <= dictionary[i].length <= 1000"
    for t in [s, *dictionary]:
        assert t.isascii() and t.isalpha() and t.islower(), (
            "s and dictionary[i] consist of lowercase English letters"
        )
