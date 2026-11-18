"""Expressive Words: a string s and a list of words, all lowercase."""


def check(s: str, words: list[str]) -> None:
    assert isinstance(s, str) and isinstance(words, list), "s is a string, words a list"
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(1 <= len(w) <= 100 for w in words), "1 <= words[i].length <= 100"
    assert all(c.isascii() and c.islower() and c.isalpha() for c in [s, *words]), (
        "s and words[i] consist of lowercase letters"
    )
