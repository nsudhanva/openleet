"""Add Bold Tag in String: a string and a list of distinct words."""

import string

ALNUM = set(string.ascii_letters + string.digits)


def check(s: str, words: list[str]) -> None:
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert 0 <= len(words) <= 100, "0 <= words.length <= 100"
    assert all(1 <= len(w) <= 1000 for w in words), "1 <= words[i].length <= 1000"
    assert set(s) <= ALNUM, "s consists of English letters and digits"
    assert all(set(w) <= ALNUM for w in words), "words[i] consist of English letters and digits"
    assert len(set(words)) == len(words), "All the values of words are unique"
