"""Weighted Word Mapping: lowercase words and 26 letter weights."""


def check(words: list[str], weights: list[int]) -> None:
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(1 <= len(w) <= 10 for w in words), "1 <= words[i].length <= 10"
    assert len(weights) == 26, "weights.length == 26"
    assert all(1 <= v <= 100 for v in weights), "1 <= weights[i] <= 100"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists of lowercase English letters"
    )
