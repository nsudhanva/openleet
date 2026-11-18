"""Minimum Number of Pushes to Type Word I: a word of distinct lowercase letters."""


def check(word: str) -> None:
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 26, "1 <= word.length <= 26"
    assert all("a" <= c <= "z" and len(c) == 1 for c in word), (
        "word consists of lowercase English letters"
    )
    assert len(set(word)) == len(word), "all letters in word are distinct"
