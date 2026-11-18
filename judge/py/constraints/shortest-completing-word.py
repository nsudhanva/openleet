"""Shortest Completing Word: a license plate string and a list of lowercase words."""

from collections import Counter


def check(licensePlate: str, words: list[str]) -> None:
    assert 1 <= len(licensePlate) <= 7, "1 <= licensePlate.length <= 7"
    assert all(ch.isascii() and (ch.isalnum() or ch == " ") for ch in licensePlate), (
        "licensePlate contains digits, letters (uppercase or lowercase), or space"
    )
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    assert all(1 <= len(w) <= 15 for w in words), "1 <= words[i].length <= 15"
    assert all("a" <= ch <= "z" for w in words for ch in w), (
        "words[i] consists of lower case English letters"
    )
    need = Counter(ch.lower() for ch in licensePlate if ch.isalpha())
    assert any(not need - Counter(w) for w in words), "It is guaranteed an answer exists"
