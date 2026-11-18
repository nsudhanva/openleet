"""Longest Palindrome by Concatenating Two Letter Words: a list of 2-letter lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 10**5, "1 <= words.length <= 10^5"
    assert all(isinstance(w, str) for w in words), "words[i] is a string"
    assert all(len(w) == 2 for w in words), "words[i].length == 2"
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consists of lowercase English letters"
    )
