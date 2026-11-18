"""Sentence Similarity II: two word lists and similar word pairs."""

import string


def check(sentence1: list[str], sentence2: list[str], similarPairs: list[list[str]]) -> None:
    letters = set(string.ascii_letters)
    assert 1 <= len(sentence1) <= 1000 and 1 <= len(sentence2) <= 1000, (
        "1 <= sentence1.length, sentence2.length <= 1000"
    )
    assert all(1 <= len(w) <= 20 and set(w) <= letters for w in sentence1 + sentence2), (
        "1 <= sentence[i].length <= 20, English letters"
    )
    assert 0 <= len(similarPairs) <= 2000, "0 <= similarPairs.length <= 2000"
    assert all(len(p) == 2 for p in similarPairs), "similarPairs[i].length == 2"
    assert all(1 <= len(w) <= 20 and set(w) <= letters for p in similarPairs for w in p), (
        "1 <= xi.length, yi.length <= 20, English letters"
    )
