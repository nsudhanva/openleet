"""Keyboard Row: a list of words of English letters."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 20, "1 <= words.length <= 20"
    assert all(1 <= len(w) <= 100 for w in words), "1 <= words[i].length <= 100"
    assert all(w.isascii() and w.isalpha() for w in words), "words[i] consists of English letters"
