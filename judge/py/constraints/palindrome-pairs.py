"""Palindrome Pairs: a list of unique lowercase words."""


def check(words: list[str]) -> None:
    assert isinstance(words, list), "words is a list"
    assert 1 <= len(words) <= 5000, "1 <= words.length <= 5000"
    assert all(isinstance(w, str) for w in words), "words[i] is a string"
    assert all(len(w) <= 300 for w in words), "0 <= words[i].length <= 300"
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consists of lowercase English letters"
    )
    assert len(set(words)) == len(words), "words are unique"
