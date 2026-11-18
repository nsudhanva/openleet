"""Bold Words in String: a list of lowercase words and a lowercase string."""

from string import ascii_lowercase

_LOWER = set(ascii_lowercase)


def check(words: list[str], s: str) -> None:
    assert 1 <= len(s) <= 500, "1 <= s.length <= 500"
    assert 0 <= len(words) <= 50, "0 <= words.length <= 50"
    assert all(1 <= len(w) <= 10 for w in words), "1 <= words[i].length <= 10"
    assert set(s) <= _LOWER, "s consists of lowercase English letters"
    assert all(set(w) <= _LOWER for w in words), "words[i] consists of lowercase English letters"
