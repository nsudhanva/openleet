"""Longest Word With All Prefixes: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 10**5, "1 <= words.length <= 10^5"
    assert all(1 <= len(w) <= 10**5 for w in words), "1 <= words[i].length <= 10^5"
    assert 1 <= sum(len(w) for w in words) <= 10**5, "1 <= sum(words[i].length) <= 10^5"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists only of lowercase English letters"
    )
