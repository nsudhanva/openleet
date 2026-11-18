"""Concatenated Words: a list of distinct lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 10**4, "1 <= words.length <= 10^4"
    assert all(1 <= len(w) <= 30 for w in words), "1 <= words[i].length <= 30"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists of only lowercase English letters"
    )
    assert len(set(words)) == len(words), "All the strings of words are unique"
    assert 1 <= sum(map(len, words)) <= 10**5, "1 <= sum(words[i].length) <= 10^5"
