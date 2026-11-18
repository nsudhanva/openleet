"""Longest Common Prefix Between Adjacent Strings After Removals: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 10**5, "1 <= words.length <= 10^5"
    assert all(isinstance(w, str) for w in words), "words[i] is a string"
    assert all(1 <= len(w) <= 10**4 for w in words), "1 <= words[i].length <= 10^4"
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consists of lowercase English letters"
    )
    assert sum(len(w) for w in words) <= 10**5, "the sum of words[i].length <= 10^5"
