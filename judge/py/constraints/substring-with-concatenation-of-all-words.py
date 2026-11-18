"""Substring with Concatenation of All Words: a lowercase string and a list of words."""


def check(s: str, words: list[str]) -> None:
    assert 1 <= len(s) <= 10**4, "1 <= s.length <= 10^4"
    assert 1 <= len(words) <= 5000, "1 <= words.length <= 5000"
    assert all(1 <= len(w) <= 30 for w in words), "1 <= words[i].length <= 30"
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters"
    assert all(all("a" <= c <= "z" for c in w) for w in words), (
        "words[i] consist of lowercase English letters"
    )
